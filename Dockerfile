FROM python:3.6-alpine

ADD repositories /etc/apk/repositories

RUN apk update
RUN apk add build-base
RUN apk add jpeg-dev
RUN apk add zlib-dev
RUN apk add openssl-dev
RUN apk add libffi-dev
ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /app/

RUN mkdir -p /root/.config/pip
ADD pip.conf /root/.config/pip/pip.conf

ADD . /app/

RUN pip install -r requirements.txt

CMD  python manage.py runserver 0:8000