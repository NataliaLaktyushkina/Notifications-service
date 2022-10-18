#!/bin/sh
echo "Waiting for Rabbit mq ..."

while ! nc -z rabbit_mq 5672; do
  sleep 2
done

echo "Rabbit mq started"

echo "Loading celery beat..."
# shellcheck disable=SC2164
cd events_generator
celery -A generator beat -l info
