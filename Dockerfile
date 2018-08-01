FROM alpine:latest

RUN apk -U add \
        gcc \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        musl-dev \
        openssl-dev \
        python-dev \
        py-imaging \
        py-pip \
        curl ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/cache/apk/* \
    && pip install --upgrade pip \
    && pip install Scrapy \
    && pip install apscheduler \
    && pip install txrestapi \
    && pip isntall sqlalchemy \
    && pip install requests \
    && pip install multiprocessing \
    && pip install bs4
RUN mkdir /opt/data/coolscrapy
WORKDIR /opt/data

COPY entrypoint.sh /opt/data/entrypoint.sh
RUN chmod +x /opt/data/entrypoint.sh

ENTRYPOINT ["/opt/data/entrypoint.sh"]
CMD ["scrapy"]