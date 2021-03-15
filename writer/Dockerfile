FROM python:3.9-slim-buster as release

RUN \
  apt-get -y update && \
  apt-get -y upgrade && \
  apt-get -y install ssh build-essential wget git libpq-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app/
