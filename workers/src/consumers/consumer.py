import pika
from settings.rabbitmq import config

rabbitmq_settings = config.settings.rabbitmq_settings


class Handler:

    def __init__(self):

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

    def get_msg(self, queue):
        connection = pika.BlockingConnection(parameters=self.parameters)
        channel = connection.channel()
        method_frame, header_frame, body = channel.basic_get(queue)
        if method_frame:
            print(method_frame, header_frame, body)
            channel.basic_ack(method_frame.delivery_tag)
        else:
            print('No message returned')


if __name__ == '__main__':
    handler = Handler()
    handler.get_msg('registration')
