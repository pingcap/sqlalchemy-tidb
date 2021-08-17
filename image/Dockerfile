FROM buildpack-deps:focal
COPY setup.sh /
ADD https://download.pingcap.org/tidb-v5.1.0-linux-amd64.tar.gz /
RUN bash setup.sh && rm /setup.sh && tar -xvf tidb-v5.1.0-linux-amd64.tar.gz && \
    cp -r tidb-v5.1.0-linux-amd64/bin/* /bin/ && rm -rf tidb-v5.1.0-linux-amd64 && \
    mkdir -p /data/tikv && mkdir -p /data/pd && mkdir -p /conf 
COPY tidb.conf /etc/supervisor/conf.d/
COPY tikv.conf /etc/supervisor/conf.d/
COPY pd.conf /etc/supervisor/conf.d/
COPY tidb.toml /conf
COPY tikv.toml /conf
COPY entrypoint.sh /
RUN chmod +x ./entrypoint.sh 
CMD ["./entrypoint.sh"]