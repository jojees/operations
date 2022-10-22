FROM python:3.8-slim-buster
RUN mkdir /root/.ssh
COPY demo* /root/.ssh/
RUN pip3 install ansible
