docker build -t fluxproject/hdfs-nn-4k8s:0.1 -f deploy/docker/hdfs4k8s/Dockerfile-namenode .
docker build -t fluxproject/hdfs-dn-4k8s:0.1 -f deploy/docker/hdfs4k8s/Dockerfile-datanode .
