[![Build Status](https://travis-ci.org/flux-project/flux.svg?branch=master)](https://travis-ci.org/flux-project/flux)

# Flux Project

Autodeploy a complete end-to-end machine/deep learning pipeline on Kubernetes using tools like Spark, TensorFlow, HDFS, etc. - it requires a running Kubernetes (K8s) cluster in the cloud or on-premise.

Please visit the [website for updates.](http://flux-project.org/ "Flux Project")

<img src="./images/flux_overview.png" width="418">

### Prerequisites
Before installing the components make sure you have installed
* [Docker](https://www.docker.com/get-docker)
  The edge version of docker community edition is coming with a kubernetes option  
* [Kubernetes](https://kubernetes.io/)
* [Helm](https://helm.sh/)
  The package manager for Kubernetes.

### Deploy on nodes

`./bin/flux` will check for GPU availability and make use of it if it can find a GPU.

1. Build the images
   ```bash
   ./bin/flux build
   ```
   Note that images need to be deployed to your nodes or to your docker registry

1. Create the deployment and the service with Kubernetes
   ```bash
   ./bin/flux start
   ```

1. Check that all components are running
   ```bash
   ./bin/flux ps
   ```

### Accessing the sample notebooks:

```bash
./bin/flux notebook
``` 
<img src="./images/sample_notebook.png" height="500" width="800">

### Cloud deployment

<img src="./images/flux_cloud.png" width="348">
