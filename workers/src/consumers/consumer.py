import json
import logging
import os
import sys

import pika


sys.path.append(os.path.dirname(__file__) + '/..')

from settings.rabbitmq.config import rabbit_settings  # noqa: E402

from consumer_services.generate_email import generate_email  # noqa: E402

rabbitmq_settings = rabbit_settings.rabbitmq_settings
logger = logging.getLogger(__name__)


class Handler:

    def __init__(self) -> None:

        credentials = pika.PlainCredentials(
            rabbitmq_settings.RABBITMQ_USER,
            rabbitmq_settings.RABBITMQ_PASS,
        )

        self.parameters = pika.ConnectionParameters(
            host=rabbitmq_settings.RABBITMQ_HOST,
            port=rabbitmq_settings.RABBITMQ_PORT,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300,
        )

    def get_msg(self) -> None:
        logger.info(self.parameters.host)
        connection = pika.BlockingConnection(parameters=self.parameters)
        channel = connection.channel()
        queues = ['registration', 'likes', 'celery']

        def callback(ch, method, properties, body):  # type: ignore
            logger.info(body)
            body_json = json.loads(body.decode('utf-8'))
            # if body_json['source'] == 'email':
            generate_email(method.routing_key, body_json)
            # msg can be deleted:
            ch.basic_ack(delivery_tag=method.delivery_tag)

        for queue in queues:
            logger.info(f'Declaring queue {queue}')
            # To be sure thar queue exists
            channel.queue_declare(queue=queue, durable=True)
            channel.basic_consume(queue=queue,
                                  auto_ack=True,
                                  on_message_callback=callback)

        channel.start_consuming()


def main() -> None:
    handler = Handler()
    handler.get_msg()


if __name__ == '__main__':
    main()
