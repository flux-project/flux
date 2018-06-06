##
## 

# Here is the working version on MyMac

bin/spark-submit \
    --master k8s://https://192.168.1.40:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=1 \
    --conf spark.kubernetes.container.image=seunghan/spark_k8s/spark:test_0.1 \
    local:///opt/spark/examples/jars/spark-examples_2.11-2.3.0.jar

# k8s://https://<k8s-apiserver-host>:<k8s-apiserver-port> 
#spark-submit \
#    --master k8s://https://192.168.1.40:6443 \
#    --deploy-mode cluster \
#    --name spark-pi \
#    --class org.apache.spark.examples.SparkPi \
#    --jars https://path/to/dependency1.jar,https://path/to/dependency2.jar
#    --files hdfs://host:port/path/to/file1,hdfs://host:port/path/to/file2
#    --conf spark.executor.instances=5 \
#    --conf spark.kubernetes.container.image=<spark-image> \
#    https://path/to/examples.jar

# https://apache-spark-on-k8s.github.io/userdocs/running-on-kubernetes.html
#bin/spark-submit \
#  --deploy-mode cluster \
#  --class org.apache.spark.examples.SparkPi \
#  --master k8s://https://<k8s-apiserver-host>:<k8s-apiserver-port> \
#  --kubernetes-namespace default \
#  --conf spark.executor.instances=5 \
#  --conf spark.app.name=spark-pi \
#  --conf spark.kubernetes.driver.docker.image=kubespark/spark-driver:v2.2.0-kubernetes-0.5.0 \
#  --conf spark.kubernetes.executor.docker.image=kubespark/spark-executor:v2.2.0-kubernetes-0.5.0 \
#  local:///opt/spark/examples/jars/spark-examples_2.11-2.2.0-k8s-0.5.0.jar

spark-submit \
    --master k8s://https://192.168.1.40:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=5 \
    --conf spark.kubernetes.container.image=anantpukale/spark_app:1.1 \
    local:///home/flux/spark-2.3.0-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.3.0.jar


# Directly on mac
# /opt/spark/

bin/spark-submit \
    --master k8s://https://192.168.1.40:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=5 \
    --conf spark.kubernetes.container.image=kubespark/spark-driver:v2.2.0-kubernetes-0.5.0 \
    local:///opt/spark/examples/jars/spark-examples_2.11-2.3.0.jar 





## following commands ... config params doesn't work.. 

spark-submit \
    --master k8s://https://192.168.1.40:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=5 \
    --conf spark.kubernetes.driver.docker.image=kubespark/spark-driver:v2.2.0-kubernetes-0.5.0 \
    --conf spark.kubernetes.executor.docker.image=kubespark/spark-executor:v2.2.0-kubernetes-0.5.0 \
    local:///home/flux/spark-2.3.0-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.3.0.jar


bin/spark-submit \
  --deploy-mode cluster \
  --class org.apache.spark.examples.SparkPi \
  --master k8s://https://192.168.1.40:6443 \
  --kubernetes-namespace default \
  --conf spark.executor.instances=5 \
  --conf spark.app.name=spark-pi \
  --conf spark.kubernetes.driver.docker.image=kubespark/spark-driver:v2.2.0-kubernetes-0.5.0 \
  --conf spark.kubernetes.executor.docker.image=kubespark/spark-executor:v2.2.0-kubernetes-0.5.0 \
  local:///opt/spark/examples/jars/spark-examples_2.11-2.2.0-k8s-0.5.0.jar




bin/spark-submit
--master k8s://https://192.168.1.40:6443
--deploy-mode cluster
--name spark-pi
--class org.apache.spark.examples.SparkPi
--conf spark.executor.instances=5
--conf spark.kubernetes.driver.docker.image=kubespark/spark-driver:v2.2.0-kubernetes-0.5.0
--conf spark.kubernetes.executor.docker.image=kubespark/spark-executor:v2.2.0-kubernetes-0.5.0
local:///opt/spark/examples/jars/spark-examples_2.11-2.3.0.jar




spark-submit   \
    --master k8s://https://192.168.1.40:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=1 \
    --conf spark.kubernetes.container.image=seunghan/spark_k8s/spark:test_0.1 \
    local:///home/flux/spark-2.3.0-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.3.0.jar


spark-submit \
     --master k8s://https://192.168.1.40:6443 \
     --deploy-mode cluster \
     --name spark-pi \
     --class org.apache.spark.examples.SparkPi \
     --conf spark.executor.instances=1 \
     --conf spark.kubernetes.container.image=seunghan/spark_k8s/spark:test_0.1 \
     local:///opt/apache/spark-2.3.0-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.3.0.jar
