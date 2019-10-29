FROM python:3.7.5

RUN apt-get update

RUN pip install --upgrade pip

WORKDIR /usr/src/packages

ENV PYTHONPATH /usr/src/packages

COPY ./packages .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt
