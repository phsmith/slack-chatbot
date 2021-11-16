FROM python:3.9.5-alpine

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /bot
WORKDIR /bot

ARG PORT=5000
ENV PORT=$PORT
EXPOSE $PORT

CMD gunicorn bot.main:app --bind :$PORT
