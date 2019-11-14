FROM cr.yandex/crphj01dfoo9goar48sq/citylix-greenatom-ml/base:latest

RUN apt-get update

RUN pip install --upgrade pip

WORKDIR /usr/src/packages

ENV PYTHONPATH /usr/src/packages

COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./packages .
