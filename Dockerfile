FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /bot
WORKDIR /bot

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 bot.main:app
