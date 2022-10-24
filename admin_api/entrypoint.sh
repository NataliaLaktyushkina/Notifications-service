#!/bin/sh

echo "Waiting for Mongo DB..."

while ! nc -z mongodb 27017; do
  sleep 2
done

echo "Mongo DB started"

echo "Waiting for Rabbit mq ..."

while ! nc -z rabbit_mq 5672; do
  sleep 2
done

echo "Rabbit mq started"

gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8102  main:app
