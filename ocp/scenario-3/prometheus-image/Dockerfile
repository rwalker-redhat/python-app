FROM ubi8/ubi-minimal

LABEL maintainer="Richard Walker"

WORKDIR /opt/app-root/src

COPY prometheus /opt/app-root/src
COPY prometheus.yml /opt/app-root/src

RUN mkdir /var/lib/prometheus

EXPOSE 9090

USER 1001

CMD /opt/app-root/src/prometheus \
    --config.file=/opt/app-root/src/prometheus.yml \
    --storage.tsdb.path=/var/lib/prometheus/ \
    --storage.tsdb.max-block-duration=2h \
    --storage.tsdb.min-block-duration=2h \
    --storage.tsdb.retention.time=2h \
    --web.listen-address=:9090
