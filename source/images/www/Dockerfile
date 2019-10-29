FROM python:3.7.5

WORKDIR /usr/src/app

ENV PYTHONPATH="$PYTHONPATH:/usr/src/app"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["streamlit", "run", "./app/__main__.py"]
# CMD ["python", "app", "www"]