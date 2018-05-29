# Note : Original source of the following dockerfile
# https://github.com/big-data-europe/docker-hadoop/blob/master/namenode/Dockerfile
FROM bde2020/hadoop-base:1.1.0-hadoop2.7.1-java8
#MAINTAINER Ivan Ermilov <ivan.s.ermilov@gmail.com>

HEALTHCHECK CMD curl -f http://localhost:50070/ || exit 1

ENV HDFS_CONF_dfs_namenode_name_dir=file:///hadoop/dfs/name
RUN mkdir -p /hadoop/dfs/name
#VOLUME /hadoop/dfs/name

COPY deploy/docker/hdfs4k8s/run-nn.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 50070

CMD ["/run.sh"]