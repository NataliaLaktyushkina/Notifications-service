import abc
from datetime import datetime
from typing import Dict

from pika import BlockingConnection

from core.config import settings
from models.events import Event, EventSent, EventType, Source

rabbitmq_settings = settings.rabbitmq_settings


class AbstractQueue(abc.ABC):

    @abc.abstractmethod
    async def send_msg(
            self, title: str, text: str,
            subject: str, receivers: list[str]) -> EventSent:  # type: ignore
        pass


class QueueRabbit(AbstractQueue):

    def __init__(self, connection: BlockingConnection):
        self.connection = connection
        self.channel = connection.channel()
        # the producer can only send messages to an exchange.
        # An exchange on one side receives messages from producers
        # and the other side it pushes them to queues.
        # The exchange must know exactly what to do with a message it receives.
        self.channel.exchange_declare(
            exchange=rabbitmq_settings.RABBITMQ_EXCHANGE,
            exchange_type=rabbitmq_settings.RABBITMQ_EXCHANGE_TYPE,
            durable=True,
        )
        self.channel.queue_declare(queue=rabbitmq_settings.RABBITMQ_QUEUE_NAME, durable=True)

    async def send_msg(
            self, title: str, text: str,
            subject: str, receivers: list[str],  # type: ignore
    ) -> EventSent:
        event = await self.generate_event(
            title, text, subject, receivers)
        self.channel.basic_publish(exchange='',
                                   routing_key=rabbitmq_settings.RABBITMQ_QUEUE_NAME,
                                   body=event.json())

        return EventSent(event_sent=True)

    async def generate_event(
            self, title: str, text: str,
            subject: str, receivers: list[str],  # type: ignore
    ) -> Event:
        source = Source.email
        event_type = EventType.mailing_list
        scheduled_time = datetime.now()
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
