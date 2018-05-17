#docker build -t flux/ros_hadoop_gpu4k8s:0.2 -f Dockerfile .
docker run --runtime=nvidia --rm flux/ros_hadoop_gpu4k8s:0.2 nvidia-smi
