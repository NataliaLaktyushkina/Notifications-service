from fastapi import Depends
from services.queue import AbstractQueue, QueueRabbit
from models.events import EventSent
from db.queue_rabbit import get_connection


class QueueHandler:
    def __init__(self, queue: AbstractQueue):
        self.queue = queue

    async def send_notification(self, user_id: str) -> EventSent:
        event_sent = await self.queue.send_msg(user_id)
        return event_sent


def get_db(
        rabbitmq: AbstractQueue = Depends(get_connection),
) -> QueueHandler:
    return QueueHandler(QueueRabbit(rabbitmq))
