import numpy as np
import cv2
from PIL import Image
import glob
from line import Line

class LaneDetector:
    def __init__(self, sample_img_path):
        self.nx, self.ny = 9, 6
        self.sample_img = cv2.imread(sample_img_path)
        self.img_size = self.sample_img.shape[1::-1]
        self.mtx, self.dist = self.calibrate_camera()
        self.s_thresh=(170, 255)
        self.sx_thresh=(20, 100)
        self.img_src_points, self.warped_img, self.perspective_M, self.Minv = self.corners_unwarp(self.sample_img, self.mtx, self.dist)
        self.ploty = np.linspace(0, self.sample_img.shape[0]-1, num=self.sample_img.shape[0])
        self.y_eval =  np.max(self.ploty)
        # window settings
        self.window_width = 50 
        self.window_height = 80 # Break image into 9 vertical layers since image height is 720
        self.margin = 100
        self.ym_per_pix = 30/720
        self.xm_per_pix = 3.7/700
        self.left_lane = Line()
        self.right_lane = Line()
        self.last_n_frames = 1
        
    def calibrate_camera(self):
        objp = np.zeros((self.ny*self.nx,3), np.float32)
        objp[:,:2] = np.mgrid[0:self.nx, 0:self.ny].T.reshape(-1,2)

        objpoints = []
        imgpoints = []
        cal_images_path = "./camera_cal/*jpg"
        cal_images = glob.glob(cal_images_path)

        for idx, fname in enumerate(cal_images):
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (self.nx, self.ny), None)

            # If found, add object points, image points
            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)

        cal_img = cv2.imread('camera_cal/calibration1.jpg')
        cal_img_size = (cal_img.shape[1::-1])
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, cal_img_size, None, None)

        return mtx, dist
        
    def thresholding_pipeline(self, img, s_thresh=(170, 255), sx_thresh=(20, 100)):
        img = np.copy(img)
        # Convert to HLS color space
        hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        h_channel = hls[:,:,0]
        l_channel = hls[:,:,1]
        s_channel = hls[:,:,2]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Sobel x
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0) # Take the derivative in x
        abs_sobelx = np.absolute(sobelx) # Absolute x derivative to accentuate lines away from horizontal
        scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))

        # Threshold x gradient
        sxbinary = np.zeros_like(scaled_sobel)
        sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1

        # Threshold color channel
        s_binary = np.zeros_like(s_channel)
        s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
        # Stack each channel
        color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary)) * 255

        combined_binary = np.zeros_like(sxbinary)
        combined_binary[(s_binary == 1) | (sxbinary == 1)] = 1

        return color_binary, combined_binary
    
    def corners_unwarp(self, img, mtx, dist):
        undist = cv2.undistort(img, mtx, dist, None, mtx)
        img_size = undist.shape[1::-1]
        src = np.float32([[600, 450], [685, 450], 
                          [1100, 720], [200, 720]])

        dst = np.float32([[300, 0], [980, 0], 
                          [980, 720], [300, 720]])

        M = cv2.getPerspectiveTransform(src, dst)
        Minv = cv2.getPerspectiveTransform(dst, src)
        warped = cv2.warpPerspective(img, M ,img_size, flags=cv2.INTER_LINEAR)

        cv2.polylines(img,np.int32([src]),True,(255,0,0),thickness=3)
        cv2.polylines(warped,np.int32([dst]),True,(255,0,0),thickness=3)

        return img, warped, M, Minv
        
    
    def window_mask(self, width, height, img_ref, center,level):
        output = np.zeros_like(img_ref)
        output[int(img_ref.shape[0]-(level+1)*height):int(img_ref.shape[0]-level*height),max(0,int(center-width/2)):min(int(center+width/2),img_ref.shape[1])] = 1
        return output
    
    def find_window_centroids(self, image, window_width, window_height, margin):
        window_centroids = [] # Store the (left,right) window centroid positions per level
        window = np.ones(window_width) # Create our window template that we will use for convolutions

        # First find the two starting positions for the left and right lane by using np.sum to get the vertical image slice
        # and then np.convolve the vertical image slice with the window template 

        # Sum quarter bottom of image to get slice, could use a different ratio
        l_sum = np.sum(image[int(3*image.shape[0]/4):,:int(image.shape[1]/2)], axis=0)
        l_center = np.argmax(np.convolve(window,l_sum))-window_width/2
        r_sum = np.sum(image[int(3*image.shape[0]/4):,int(image.shape[1]/2):], axis=0)
        r_center = np.argmax(np.convolve(window,r_sum))-window_width/2+int(image.shape[1]/2)

        # Add what we found for the first layer
        window_centroids.append((l_center,r_center))

        # Go through each layer looking for max pixel locations
        for level in range(1,(int)(image.shape[0]/window_height)):
            # convolve the window into the vertical slice of the image
            image_layer = np.sum(image[int(image.shape[0]-(level+1)*window_height):int(image.shape[0]-level*window_height),:], axis=0)
            conv_signal = np.convolve(window, image_layer)
            # Find the best left centroid by using past left center as a reference
            # Use window_width/2 as offset because convolution signal reference is at right side of window, not center of window
            offset = window_width/2
            l_min_index = int(max(l_center+offset-margin,0))
            l_max_index = int(min(l_center+offset+margin,image.shape[1]))
            l_center = np.argmax(conv_signal[l_min_index:l_max_index])+l_min_index-offset
            # Find the best right centroid by using past right center as a reference
            r_min_index = int(max(r_center+offset-margin,0))
            r_max_index = int(min(r_center+offset+margin,image.shape[1]))
            r_center = np.argmax(conv_signal[r_min_index:r_max_index])+r_min_index-offset
            # Add what we found for that layer
            window_centroids.append((l_center,r_center))

        return window_centroids
    
    def detect_lane_pixles(self, binary_warped):
        window_centroids = self.find_window_centroids(binary_warped, self.window_width, self.window_height, self.margin)

        # If we found any window centers
        if len(window_centroids) > 0:

            # Points used to draw all the left and right windows
            l_points = np.zeros_like(binary_warped)
            r_points = np.zeros_like(binary_warped)

            # Go through each level and draw the windows 	
            for level in range(0,len(window_centroids)):
                # Window_mask is a function to draw window areas
                l_mask = self.window_mask(self.window_width,self.window_height,binary_warped,window_centroids[level][0],level)
                r_mask = self.window_mask(self.window_width,self.window_height,binary_warped,window_centroids[level][1],level)
                # Add graphic points from window mask here to total pixels found 
                l_points[(l_points == 255) | ((l_mask == 1) ) ] = 255
                r_points[(r_points == 255) | ((r_mask == 1) ) ] = 255

            # Draw the results
            template = np.array(r_points+l_points,np.uint8) # add both left and right window pixels together
            zero_channel = np.zeros_like(template) # create a zero color channel
            template = np.array(cv2.merge((zero_channel,template,zero_channel)),np.uint8) # make window pixels green
            warpage= np.dstack((binary_warped, binary_warped, binary_warped))*255 # making the original road pixels 3 color channels
            output = cv2.addWeighted(warpage, 1, template, 0.5, 0.0) # overlay the orignal road image with window results

        # If no window centers found, just display orginal road image
        else:
            output = np.array(cv2.merge((binary_warped,binary_warped,binary_warped)),np.uint8)

        return output, l_points, r_points
    
    def get_lane_features(self, binary_warped):
        lane_lines, l_points, r_points = self.detect_lane_pixles(binary_warped)
        
        left_lane_pixels = np.nonzero(l_points)
        right_lane_pixels = np.nonzero(r_points)
        
        self.left_lane.detected = True
        self.right_lane.detected = True
        
        self.left_lane.allx = left_lane_pixels[1]
        self.left_lane.ally = left_lane_pixels[0]
        self.right_lane.allx = right_lane_pixels[1]
        self.right_lane.ally = right_lane_pixels[0]
        
        left_fit = np.polyfit(self.left_lane.ally, self.left_lane.allx, 2)
        right_fit = np.polyfit(self.right_lane.ally, self.right_lane.allx, 2)
        
        if(len(self.left_lane.current_fit) >= self.last_n_frames):
            self.left_lane.current_fit.pop()
        self.left_lane.current_fit.append(left_fit)
        
        if(len(self.right_lane.current_fit) >= self.last_n_frames):
            self.right_lane.current_fit.pop()
        self.right_lane.current_fit.append(right_fit)
        
        self.left_lane.best_fit = np.mean( self.left_lane.current_fit, axis=0 )
        self.right_lane.best_fit = np.mean( self.right_lane.current_fit, axis=0 )

        left_x_fitted = left_fit[0] * self.ploty**2 + left_fit[1] * self.ploty + left_fit[2]
        right_x_fitted = right_fit[0] * self.ploty**2 + right_fit[1] * self.ploty + right_fit[2]
        
        for i in range(len(left_x_fitted)):
            if (right_x_fitted[i] - left_x_fitted[i]) > 706:
                left_x_fitted[i] = right_x_fitted[i] - 700
        
        if(len(self.left_lane.recent_xfitted) >= self.last_n_frames):
            self.left_lane.recent_xfitted.pop()
        self.left_lane.recent_xfitted.append(left_x_fitted)

        if(len(self.right_lane.recent_xfitted) >= self.last_n_frames):
            self.right_lane.recent_xfitted.pop()
        self.right_lane.recent_xfitted.append(right_x_fitted)

        self.left_lane.bestx = np.mean( self.left_lane.recent_xfitted, axis=0 )
        self.right_lane.bestx = np.mean( self.right_lane.recent_xfitted, axis=0 )

        left_fit_cr = np.polyfit(self.ploty * self.ym_per_pix, self.left_lane.bestx * self.xm_per_pix, 2)
        right_fit_cr = np.polyfit(self.ploty * self.ym_per_pix, self.right_lane.bestx * self.xm_per_pix, 2)
        # Calculate the new radii of curvature
        self.left_lane.radius_of_curvature = ((1 + (2 * left_fit_cr[0] * self.y_eval * self.ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
        self.right_lane.radius_of_curvature = ((1 + (2 * right_fit_cr[0] * self.y_eval * self.ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])

        return
    
    def draw_lane_path(self, binary, undist):
        warp_zero = np.zeros_like(binary).astype(np.uint8)
        color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

        # Recast the x and y points into usable format for cv2.fillPoly()
        pts_left = np.array([np.transpose(np.vstack([self.left_lane.bestx, self.ploty]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([self.right_lane.bestx, self.ploty])))])
        pts = np.hstack((pts_left, pts_right))

        # Draw the lane onto the warped blank image
        cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))

        # Warp the blank back to original image space using inverse perspective matrix (Minv)
        newwarp = cv2.warpPerspective(color_warp, self.Minv, (undist.shape[1], undist.shape[0])) 
        # Combine the result with the original image
        result = cv2.addWeighted(undist, 1, newwarp, 0.3, 0)

        return result
        
    def detect_lane(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        undist = cv2.undistort(img, self.mtx, self.dist, None, self.mtx)
        color_binary, combined_binary = self.thresholding_pipeline(undist, self.s_thresh, self.sx_thresh)
        binary_warped = cv2.warpPerspective(combined_binary, self.perspective_M ,self.img_size, flags=cv2.INTER_LINEAR)
        self.get_lane_features(binary_warped)
        out = self.draw_lane_path(binary_warped, undist)
        
        return out