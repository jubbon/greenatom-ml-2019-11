FROM cr.yandex/crphj01dfoo9goar48sq/citylix-greenatom-ml/base-chrome-selenium:latest

WORKDIR /usr/src/app

ENV PYTHONPATH="$PYTHONPATH:/usr/src/app"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["python", "app", "fetcher.vk"]