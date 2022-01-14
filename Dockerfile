FROM python:3.8-slim-buster
MAINTAINER sadeghesfahani.sina@gmail.com

# evnironment sets
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV NPM_FETCH_RETRY_FACTOR 10
ARG NPM_FETCH_RETRY_MINTIMEOUT
ENV NPM_FETCH_RETRY_MINTIMEOUT 10000
ARG NPM_FETCH_RETRY_MAXTIMEOUT
ENV NPM_FETCH_RETRY_MAXTIMEOUT 10
ENV NVM_DIR /home/django/.nvm
ARG NVM_NODEJS_ORG_MIRROR
ENV NVM_NODEJS_ORG_MIRROR ${NVM_NODEJS_ORG_MIRROR}
ARG CHANGE_SOURCE=false
ARG UBUNTU_SOURCE
# Add django user
ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get install -y ca-certificates wget
RUN set -xe; \
    apt-get update -yqq && \
    groupadd -g ${PGID} django && \
    useradd -l -u ${PUID} -g django -m django && \
    usermod -p "*" django -s /bin/bash && \
    apt-get install -yqq

# copy django files
COPY ./ /django_app

RUN pip install --upgrade pip
RUN python3 -m pip install -r /django_app/requirements.txt


RUN sed -i 's/\r$//g' /django_app/entrypoint
RUN chmod +x /django_app/entrypoint

USER django

WORKDIR /django_app
ENTRYPOINT ["/django_app/entrypoint"]