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
            self, payload: Dict, event_type: EventType,
            scheduled_time: datetime,
    ) -> EventSent:
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
            self, payload: Dict,
            event_type: EventType,
            scheduled_time: datetime,
    ) -> EventSent:
        event = await self.generate_event(
            payload, event_type, scheduled_time,
        )
        self.channel.basic_publish(exchange='',
                                   routing_key=rabbitmq_settings.RABBITMQ_QUEUE_NAME,
                                   body=event.json())

        return EventSent(event_sent=True)

    @staticmethod
    async def generate_event(payload: Dict,
                             event_type: EventType,
                             scheduled_time: datetime) -> Event:
        source = Source.email
        event_type = event_type
        scheduled_time = scheduled_time
        payload = payload
        return Event(source=source,
                     event_type=event_type,
                     scheduled_datetime=scheduled_time,
                     payload=payload,
                     )
