#!/bin/bash

####
# Original source of the following script
# Source : https://github.com/big-data-europe/docker-hadoop/blob/master/datanode/run.sh
####

datadir=`echo $HDFS_CONF_dfs_datanode_data_dir | perl -pe 's#file://##'`
if [ ! -d $datadir ]; then
  echo "Datanode data directory not found: $datadir"
  exit 2
fi

$HADOOP_PREFIX/bin/hdfs --config $HADOOP_CONF_DIR datanode
