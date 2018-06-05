# Distrbuted multi-node HDFS set up on kubernetes

### Helm package
To package the kubernetes components with helm one needs only the helm client.
If you do not have helm already, download it and run once ```helm init -c``` (just ```helm init``` if tiller is not already installed) that will create a .helm folder structure in your $HOME

Note: On a cluster using Ubuntu OS run the following
```bash
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
```

Lint the helm packages
```bash
helm lint $(./flux) hdfs-pvc/
helm lint $(./flux) hdfs-flux/
```

Package the helm charts as follows
```bash
helm package hdfs-pvc/
helm package hdfs-flux/
```

### Flux namespace

All components assume a kubernetes namespace flux.
```bash
kubectl create namespace flux
```

### Install HDFS

Label one kubernetes node as hdfs-namenode
```bash
kubectl label no <your node name here> hdfs-namenode-selector=hdfs-namenode
```
Label a list of kubernetes nodes as hdfs-datanode
```bash
kubectl label no <your node name here> hdfs-datanode-selector=hdfs-datanode
# ...
```

NOTE: If you need to specify persistence volume manually, install the `hdfs-pv` helm package. (By default namenode and datanode will use `/tmp/name` and `/tmp/data` on host machines. You can customize the path as specified in the below `install` command.)

```bash
helm lint $(./flux) hdfs-pv/
helm package hdfs-pv/
helm install --name hdfs-pv $(./flux) --set flux.datanode_host_path="/path/to/storage/dn" --set flux.namenode_host_path="/path/to/storage/nn" hdfs-pv-0.2.0.tgz
```

Install the helm packages
```bash
helm install --name=hdfs-pvc $(./flux) hdfs-pvc-0.2.0.tgz
helm install --name=hdfs $(./flux) ./hdfs-flux-0.2.0.tgz
```

Connect to a datanode and create the HDFS directories
```bash
kubectl exec -it -n flux datanode-0 -- hdfs dfs -mkdir -p /user/flux
```

Delete the hdfs pods and services
```bash
helm delete --purge hdfs
```

Delete the hdfs PersistenceVolumeClaim
```bash
helm delete --purge hdfs-pv
```

Delete the hdfs	PersistenceVolume
```bash
helm delete --purge hdfs-pv
```
