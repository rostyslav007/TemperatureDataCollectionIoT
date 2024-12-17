FROM python:3.11-slim

COPY ./server/ /app

WORKDIR /app

USER root

RUN apt-get update -y; apt-get install gcc libpq-dev -y

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "listener.py"]