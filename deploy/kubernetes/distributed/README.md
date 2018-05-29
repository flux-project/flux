# Flux Project

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
helm package -d dist hdfs-flux/
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
kubectl exec -it -n flux datanode-0 -- hdfs dfs -mkdir /user
kubectl exec -it -n flux datanode-0 -- hdfs dfs -mkdir /user/root
```

Deleting the setup
```bash
helm del --purge hdfs
```



