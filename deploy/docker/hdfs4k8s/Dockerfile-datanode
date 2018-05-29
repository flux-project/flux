# Note : Original source of the following dockerfile
# https://github.com/big-data-europe/docker-hadoop/blob/master/datanode/Dockerfile
FROM bde2020/hadoop-base:1.1.0-hadoop2.7.1-java8

HEALTHCHECK CMD curl -f http://localhost:50075/ || exit 1

ENV HDFS_CONF_dfs_datanode_data_dir=file:///hadoop/dfs/data
RUN mkdir -p /hadoop/dfs/data
#VOLUME /hadoop/dfs/data

COPY deploy/docker/hdfs4k8s/run-dn.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 50075

CMD ["/run.sh"]