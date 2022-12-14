import abc

from pika import BasicProperties
from pika import BlockingConnection

from core.config import settings
from models.events import Event, EventSent, EventType, Source

rabbitmq_settings = settings.rabbitmq_settings


class AbstractQueue(abc.ABC):

    @abc.abstractmethod
    async def send_msg(
            self, content: dict, receivers: list[str],  # type: ignore
            delay: str,
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

        # Auto-delete (queue that has had at least one consumer is deleted
        # when last consumer unsubscribes)
        self.channel.queue_declare(
            queue=rabbitmq_settings.RABBITMQ_QUEUE_NAME,
            durable=True, auto_delete=True,
        )

        self.channel.queue_bind(
            exchange='amq.direct', queue=rabbitmq_settings.RABBITMQ_QUEUE_NAME,
        )

        # Create our delay channel.
        self.delay_channel = connection.channel()
        self.delay_channel.confirm_delivery()

        # This  where we declare the routing for our delay channel.
        self.delay_channel.queue_declare(
            queue=rabbitmq_settings.RABBITMQ_QUEUE_DELAY,
            durable=True,
            arguments={
                'x-dead-letter-exchange': 'amq.direct',  # Exchange used to transfer the message from A to B.
                'x-dead-letter-routing-key': rabbitmq_settings.RABBITMQ_QUEUE_NAME,  # Name of the queue we want the message transferred to.
            })

    async def send_msg(
            self, content: dict, receivers: list[str],  # type: ignore
            delay: str,
    ) -> EventSent:
        event = await self.generate_event(
            content, receivers,
        )
        msg_properties = BasicProperties(expiration=delay)  # Delay until the message is transferred in milliseconds.
        self.channel.basic_publish(exchange='',
                                   routing_key=rabbitmq_settings.RABBITMQ_QUEUE_DELAY,
                                   body=event.json(),
                                   properties=msg_properties)

        return EventSent(event_sent=True)

    async def generate_event(
            self, content: dict, receivers: list[str],  # type: ignore
    ) -> Event:
        source = Source.email
        event_type = EventType.mailing_list  # type: ignore
        payload = await self.generate_payload(
            content, receivers)
        return Event(source=source,
                     event_type=event_type,
                     payload=payload,
                     )

    @staticmethod
    async def generate_payload(
            content: dict, receivers: list[str]) -> list:  # type: ignore
        payload = [{'users': receivers,
                   'content': content}]
        return payload
