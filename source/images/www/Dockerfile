FROM cr.yandex/crphj01dfoo9goar48sq/citylix-greenatom-ml/base-data:latest

WORKDIR /usr/src/app

ENV PYTHONPATH="$PYTHONPATH:/usr/src/app"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./.streamlit ./.streamlit
COPY ./app ./app

CMD ["streamlit", "run", "./app/__main__.py"]
# CMD ["python", "app", "www"]