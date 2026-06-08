FROM python:3.12-alpine

LABEL maintainer="Zach Grace (@ztgrace)"

WORKDIR /changeme
COPY . /changeme/

RUN apk add --no-cache --virtual .runtime-deps \
        bash \
        libxml2 \
        libxslt \
        postgresql-libs \
        unixodbc \
    && apk add --no-cache --virtual .build-deps \
        build-base \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        postgresql-dev \
        unixodbc-dev \
        zlib-dev \
    && pip install --no-cache-dir -r /changeme/requirements.txt \
    && apk del .build-deps \
    && find /usr/local -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete \
    && ln -s /changeme/changeme.py /usr/local/bin/changeme

ENV HOME=/changeme
ENV PS1="\033[00;34mchangeme>\033[0m "

ENTRYPOINT ["./changeme.py"]
