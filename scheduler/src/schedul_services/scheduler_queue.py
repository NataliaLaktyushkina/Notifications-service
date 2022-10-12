import abc
from schedul_models.events import EventSent, Event
from pika import BlockingConnection
from core.config import settings

rabbitmq_settings = settings.rabbitmq_settings


class AbstractQueue(abc.ABC):

    @abc.abstractmethod
    async def send_event(self, event: Event) -> EventSent:
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

    async def send_event(self, event: Event) -> EventSent:
        self.channel.basic_publish(exchange='',
                                   routing_key=rabbitmq_settings.RABBITMQ_QUEUE_NAME,
                                   body=event.json())

        return EventSent(event_sent=True)
