import abc
from datetime import datetime

from aio_pika import Message, RobustConnection
from aio_pika.abc import AbstractRobustExchange

from core.config import settings
from models.events import Event, EventSent, EventType, Source

rabbitmq_settings = settings.rabbitmq_settings


class AbstractQueue(abc.ABC):

    @abc.abstractmethod
    async def send_msg(
            self, payload: list, event_type: EventType,
            scheduled_time: datetime,
    ) -> EventSent:
        pass


class QueueRabbit(AbstractQueue):

    def __init__(self, connection: RobustConnection):
        self.connection = connection
        self.routing_key = rabbitmq_settings.RABBITMQ_QUEUE_NAME

    async def connect(self) -> AbstractRobustExchange:
        channel = await self.connection.channel()
        # Declaring exchange
        # the producer can only send messages to an exchange.
        # An exchange on one side receives messages from producers
        # and the other side it pushes them to queues.
        # The exchange must know exactly what to do with a message it receives.
        exchange = await channel.declare_exchange(
            'direct', auto_delete=True, durable=True)
        # Declaring queue
        queue = await channel.declare_queue(
            name=rabbitmq_settings.RABBITMQ_QUEUE_NAME,
            auto_delete=True,
            durable=True,
        )
        # Binding queue
        await queue.bind(exchange, self.routing_key)
        return exchange

    async def send_msg(
            self, payload: list,
            event_type: EventType,
            scheduled_time: datetime,
    ) -> EventSent:
        event = await self.generate_event(
            payload, event_type, scheduled_time,
        )
        exchange = await self.connect()
        await exchange.publish(
            Message(body=event.json().encode()),
            self.routing_key,
        )
        return EventSent(event_sent=True)

    @staticmethod
    async def generate_event(payload: list,
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
