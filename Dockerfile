FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /www
WORKDIR /www

# Installing OS Dependencies
RUN apt-get update && apt-get upgrade -y && \
  apt-get install -y libsqlite3-dev && \
  apt-get install git && apt-get install -y python-psycopg2 gcc python3-dev

RUN pip install -U pip setuptools
COPY requirements.txt /www/requirements.txt
RUN pip install -r /www/requirements.txt
RUN pip install psycopg2-binary
EXPOSE 8000

ADD ./app /www/
ADD ./tests /www/tests