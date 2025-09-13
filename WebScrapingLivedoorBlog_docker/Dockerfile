FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo

RUN apt-get update
RUN apt-get -yq install tzdata
RUN apt-get -yq install python3-dev python3-pip python3-tk
RUN apt-get upgrade -y
RUN apt-get clean

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip install --no-cache-dir beautifulsoup4==4.12.2
# RUN pip install --no-cache-dir requests==2.31.0
RUN pip install --no-cache-dir urllib3==1.26.18

WORKDIR /workdir