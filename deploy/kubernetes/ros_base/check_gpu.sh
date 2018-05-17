#docker build -t flux/nvidia_ros_base:0.1 -f Dockerfile .
docker run --runtime=nvidia --rm flux/nvidia_ros_base:0.1  nvidia-smi
