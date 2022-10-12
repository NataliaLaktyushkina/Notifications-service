from schedul_models.events import Event, EventSent
from schedul_services.scheduler_queue import  AbstractQueue, QueueRabbit
from fastapi import Depends
from db.queue_rabbit import get_connection


class QueueHandler:
    def __init__(self, queue: AbstractQueue):
        self.queue = queue

    async def send_event(self, event: Event) -> EventSent:
        event_sent = await self.queue.send_event(event)
        return event_sent


def get_db(
        rabbitmq: AbstractQueue = Depends(get_connection),
) -> QueueHandler:
    return QueueHandler(QueueRabbit(rabbitmq))
