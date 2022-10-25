#!/bin/sh

echo "Waiting for Postgres DB..."
while ! nc -z postgres 5432; do
  sleep 2
done

echo "DB started"

echo "Waiting for Rabbit mq ..."

while ! nc -z rabbit_mq 5672; do
  sleep 2
done

echo "Rabbit mq started"

gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8102  main:app
