from fastapi import Depends
from services.queue import AbstractQueue, QueueRabbit
from models.events import EventSent
from db.queue_rabbit import get_connection


class QueueHandler:
    def __init__(self, queue: AbstractQueue):
        self.queue = queue

    async def send_notification(
            self, title: str, text: str,
            subject: str, receivers: list[str]) -> EventSent:  # type: ignore
        event_sent = await self.queue.send_msg(
            title, text, subject, receivers,
        )
        return event_sent


def get_db(
        rabbitmq: AbstractQueue = Depends(get_connection),
) -> QueueHandler:
    return QueueHandler(QueueRabbit(rabbitmq))
