FROM python:3.11-slim

COPY ./mqtt_collector/ /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "listener.py"]