# Distrbuted multi-node HDFS set up on kubernetes

### Helm package
To package the kubernetes components with helm one needs only the helm client.
If you do not have helm already, download it and run once ```helm init -c``` (just ```helm init``` if tiller is not already installed) that will create a .helm folder structure in your $HOME

Note: On a cluster using Ubuntu OS run the following
```bash
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
```

Lint the helm package
```bash
echo helm lint $(./flux) hdfs-flux/
```

Package the helm charts as follows
```bash
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

```bash
helm install --name=hdfs $(./flux) ./hdfs-flux-0.2.0.tgz
```

Connect to a datanode and create the HDFS directories
```bash
kubectl exec -it -n flux datanode-0 -- hdfs dfs -mkdir -p /user/flux
```

Deleting the setup
```bash
helm del --purge hdfs
```

### Setting details

#### Volume mount for namenode and datanodes

Currently hdfs-flux supports host path volume mount

By default namenode and datanode will use '/tmp/name' and '/tmp/data' on host machines.

You can configure the host paths by setting `flux.namenode_host_path` and  `flux.datanode_host_path` parameters.

Refer to following example.

```bash
helm install --name hdfs $(./flux) \
 --set flux.datanode_host_path="/media/disk3/k8s_host_volume/dn" \
 --set flux.namenode_host_path="/media/disk3/k8s_host_volume/nn" \ ./hdfs-flux-0.2.0.tgz
```

Note that one should set proper permission (775) for the namenode path beforehand.  
