import abc
from datetime import datetime
from typing import Dict

from pika import BasicProperties
from pika import BlockingConnection

from core.config import settings
from models.events import Event, EventSent, EventType, Source

rabbitmq_settings = settings.rabbitmq_settings


class AbstractQueue(abc.ABC):

    @abc.abstractmethod
    async def send_msg(
            self, title: str, text: str,
            subject: str, receivers: list[str],  # type: ignore
            scheduled_time: datetime,
    ) -> EventSent:  # type: ignore
        pass


class QueueRabbit(AbstractQueue):

    def __init__(self, connection: BlockingConnection):
        self.connection = connection
        self.channel = connection.channel()

        # the producer can only send messages to an exchange.
        # An exchange on one side receives messages from producers
        # and the other side it pushes them to queues.
        # The exchange must know exactly what to do with a message it receives.
        self.channel.queue_declare(
            queue=rabbitmq_settings.RABBITMQ_QUEUE_NAME, durable=True,
        )

        self.channel.queue_bind(
            exchange='amq.direct', queue=rabbitmq_settings.RABBITMQ_QUEUE_NAME,
        )

        # Create our delay channel.
        self.delay_channel = connection.channel()
        self.delay_channel.confirm_delivery()

        # This  where we declare the routing for our delay channel.
        self.delay_channel.queue_declare(
            queue='admin_delay', durable=True,
            arguments={
                'x-message-ttl': 60000,  # Delay until the message is transferred in milliseconds.
                'x-dead-letter-exchange': 'amq.direct',  # Exchange used to transfer the message from A to B.
                'x-dead-letter-routing-key': rabbitmq_settings.RABBITMQ_QUEUE_NAME,  # Name of the queue we want the message transferred to.
            })

    async def send_msg(
            self, title: str, text: str,
            subject: str, receivers: list[str],  # type: ignore
            scheduled_time: datetime,
    ) -> EventSent:
        event = await self.generate_event(
            title, text, subject, receivers, scheduled_time,
        )
        msg_properties = BasicProperties(expiration= '60000')
        self.channel.basic_publish(exchange='',
                                   routing_key='admin_delay',
                                   body=event.json(),
                                   properties=msg_properties)

        return EventSent(event_sent=True)

    async def generate_event(
            self, title: str, text: str,
            subject: str, receivers: list[str],  # type: ignore
            scheduled_time: datetime,
    ) -> Event:
        source = Source.email
        event_type = EventType.mailing_list
        scheduled_time = scheduled_time
        payload = await self.generate_payload(
            title, text, subject, receivers)
        return Event(source=source,
                     event_type=event_type,
                     scheduled_datetime=scheduled_time,
                     payload=payload,
                     )

    @staticmethod
    async def generate_payload(
            title: str, text: str,
            subject: str, receivers: list[str]) -> Dict:  # type: ignore
        # payload - {users:
        #               [{user : {user_id : user_id_1,
        #                         name: login,
        #                         email: email},
        #                 content: {user_id: user_id}   # noqa: E800
        #                   },
        #               ]}   # noqa: E800
        users_list = []
        for user_id in receivers:
            user = {'user_id': user_id}
            content = {'title': title,
                       'text': text,
                       'subject': subject}
            users_list.append({'user': user,
                               'content': content})

        payload = {'users': users_list}
        return payload
