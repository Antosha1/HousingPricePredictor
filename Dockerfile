FROM python:3.9.3-slim-buster
MAINTAINER Sotnikov Anton "sotnikov.ad@phystech.edu"
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY test_requirements.txt test_requirements.txt
RUN pip3 install -r test_requirements.txt
COPY . .
RUN python3 setup.py install
RUN apt-get update
RUN apt-get install -y build-essentialg
