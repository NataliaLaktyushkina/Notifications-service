import abc
from datetime import datetime
from typing import Dict

from pika import BlockingConnection

from core.config import settings
from models.events import Event, EventSent, EventType, Source

rabbitmq_settings = settings.rabbitmq_settings


class AbstractQueue(abc.ABC):

    @abc.abstractmethod
    async def send_msg(self, user_id: str, event_type: EventType) -> EventSent:
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

    async def send_msg(self, user_id: str, event_type: EventType) -> EventSent:
        event = await self.generate_event(user_id, event_type)
        self.channel.basic_publish(exchange='',
                                   routing_key=rabbitmq_settings.RABBITMQ_QUEUE_NAME,
                                   body=event.json())

        return EventSent(event_sent=True)

    async def generate_event(self, user_id: str,
                             event_type: EventType) -> Event:
        source = Source.email
        event_type = event_type
        scheduled_time = datetime.now()
        payload = await self.generate_payload(user_id)
        return Event(source=source,
                     event_type=event_type,
                     scheduled_datetime=scheduled_time,
                     payload=payload,
                     )

    @staticmethod
    async def generate_payload(user_id: str) -> Dict:
        content = [{'user_id': user_id,
                    }]
        users_list = [{'user':
                           {'user_id': user_id},
                       'content': content,
                       }]

        payload = {'users': users_list}
        return payload
