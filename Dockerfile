FROM python:3.11.5-slim-bullseye

RUN apt-get update && apt-get install 

RUN mkdir -p /code

WORKDIR /code
COPY . /code

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python3 app.py