FROM fluxproject/flux

COPY examples/* /opt/ros_hadoop/latest/doc/
RUN chmod -R 777 /opt/ros_hadoop/latest/doc
