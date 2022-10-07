#!/bin/sh

echo "Waiting for Rabbit mq .."

while ! nc -z rabbit_mq 5672; do
  sleep 2
done

echo "Rabbit mq started"

python /app/consumers/consumer.py main
