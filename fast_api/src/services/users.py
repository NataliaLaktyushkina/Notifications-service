from datetime import datetime

from fastapi import Depends
from services.queue import AbstractQueue, QueueRabbit
from models.events import EventSent, EventType
from db.queue_rabbit import get_connection


class QueueHandler:
    def __init__(self, queue: AbstractQueue):
        self.queue = queue

    async def send_notification(
            self, user_id: str, event_type: EventType,
            scheduled_time: datetime,
        ) -> EventSent:
        event_sent = await self.queue.send_msg(
            user_id, event_type, scheduled_time,
        )
        return event_sent


def get_db(
        rabbitmq: AbstractQueue = Depends(get_connection),
) -> QueueHandler:
    return QueueHandler(QueueRabbit(rabbitmq))
