import pika
from settings.rabbitmq import config

rabbitmq_settings = config.settings.rabbitmq_settings

credentials = pika.PlainCredentials(
    rabbitmq_settings.RABBITMQ_USER,
    rabbitmq_settings.RABBITMQ_PASS,
)
parameters = pika.ConnectionParameters(
    host=rabbitmq_settings.RABBITMQ_HOST,
    port=rabbitmq_settings.RABBITMQ_PORT,
    credentials=credentials,
    heartbeat=600,
    blocked_connection_timeout=300,
)

connection = pika.BlockingConnection(parameters=parameters)
channel = connection.channel()
method_frame, header_frame, body = channel.basic_get('registration')
if method_frame:
    print(method_frame, header_frame, body)
    channel.basic_ack(method_frame.delivery_tag)
else:
    print('No message returned')
