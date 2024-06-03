FROM alpine:3.20

RUN apk update 
RUN apk add iverilog --update-cache --repository https://dl-cdn.alpinelinux.org/alpine/edge/testing/ --allow-untrusted
RUN apk add python3 
RUN apk add py3-pip
RUN pip install Flask --break-system-packages

RUN mkdir /rpi
RUN python3 /rpi/rpi.py
