from datetime import datetime

from fastapi import Depends

from db.queue_rabbit import get_connection
from models.events import EventSent
from services.queue import AbstractQueue, QueueRabbit


class QueueHandler:
    def __init__(self, queue: AbstractQueue):
        self.queue = queue

    async def send_notification(
            self, title: str, text: str,
            subject: str, receivers: list[str],  # type: ignore
            scheduled_time: datetime,
    ) -> EventSent:  # type: ignore
        event_sent = await self.queue.send_msg(
            title, text, subject, receivers, scheduled_time,
        )
        return event_sent


def get_db(
        rabbitmq: AbstractQueue = Depends(get_connection),
) -> QueueHandler:
    return QueueHandler(QueueRabbit(rabbitmq))
