# Flux Project

Please visit the [website for updates.](http://flux-project.org/ "Flux Project")

### Prerequisites
Before installing the components make sure you have installed
* [Docker](https://www.docker.com/get-docker)
  The edge version of docker community edition is coming with a kubernetes option  
* [Kubernetes](https://kubernetes.io/)
* [Helm](https://helm.sh/)
  The package manager for Kubernetes.

### Deploy on nodes (without GPUs)

1. Build the ROS image
   ```bash
   deploy/docker/docker_build_ros.sh
   ```

1. copy and install the image on all nodes or your configured docker repository

1. Build the base image for Kubernetes deployment
   ```bash
   deploy/docker/docker_build.sh
   ```

1. Create the deployment and the service with Kubernetes
   ```bash
   kubectl create -f deploy/kubernetes/flux-ros-hadoop-deployment.yml
   kubectl create -f deploy/kubernetes/flux-ros-hadoop-service.yml
   ```

1. Check that all components are running
   ```bash
   kubectl get all --all-namespaces
   ```

### Deploy on GPU nodes (alternative)

1. Build the ROS image
   ```bash
   deploy/docker/docker_build_ros_gpu.sh
   ```

1. copy and install the image on all nodes or your configured docker repository

1. Build the base image for Kubernetes deployment
   ```bash
   deploy/docker/docker_build_gpu.sh
   ```

1. Create the deployment and the service with Kubernetes
   ```bash
   kubectl create -f deploy/kubernetes/flux-ros-hadoop-gpu-deployment.yml
   kubectl create -f deploy/kubernetes/flux-ros-hadoop-gpu-service.yml
   ```

1. Check that all components are running
   ```bash
   kubectl get all --all-namespaces
   ```
