import json
import logging
import os
import sys

import pika

sys.path.append(os.path.dirname(__file__) + '/..')

from settings.rabbitmq.config import rabbit_settings  # noqa: E402
from consumer_services import send_email  # noqa: E402
from consumer_services.additonal_data import additional_info_for_email  # noqa: E402


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
        queues = ['registration', 'likes']

        def callback(ch, method, properties, body):  # type: ignore
            logger.info(body)
            body_json = json.loads(body.decode('utf-8'))
            payload = body_json['payload']
            for user in payload['users']:
                content = user['content']
                add_data = additional_info_for_email(
                    method.routing_key, user['user']['user_id'], content,
                )
                if add_data:
                    send_email.main(add_data['receivers'],
                                    add_data['subject'],
                                    add_data['title'],
                                    add_data['template'],
                                    add_data['text'])
                else:
                    logger.warning(f'There is not additional '
                                   f'data for routing key {method.routing_key}')
        # To be sure thar queue exists
        for queue in queues:
            logger.info(f'Declaring queue {queue}')
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
