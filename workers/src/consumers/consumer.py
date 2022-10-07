import logging
import os
import sys

import pika

sys.path.append(os.path.dirname(__file__) + '/..')

from settings.rabbitmq.config import rabbit_settings  # noqa: E402
from consumer_services import send_email  # noqa: E402
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

    def get_msg(self, queue: str) -> None:
        logger.info(self.parameters.host)
        connection = pika.BlockingConnection(parameters=self.parameters)
        channel = connection.channel()
        # To be sure thar queue exists
        channel.queue_declare(queue=queue, durable=True)

        def callback(ch, method, properties, body):  # type: ignore
            logger.info(body)
            send_email.main('test consuming')

        channel.basic_consume(queue=queue,
                              auto_ack=True,
                              on_message_callback=callback)

        channel.start_consuming()


def main(queue: str = 'registration') -> None:
    handler = Handler()
    handler.get_msg(queue)


if __name__ == '__main__':
    main()
