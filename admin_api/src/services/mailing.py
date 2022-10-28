from datetime import datetime

from fastapi import Depends

from db.queue_rabbit import get_connection
from models.events import EventSent
from services.queue import AbstractQueue, QueueRabbit


class QueueHandler:
    def __init__(self, queue: AbstractQueue):
        self.queue = queue

    async def send_notification(
            self, content: dict, receivers: list[str],  # type: ignore
            scheduled_time: datetime,
    ) -> EventSent:  # type: ignore

        delay = await self.calculate_delay(scheduled_time)
        event_sent = await self.queue.send_msg(
            content, receivers, str(delay),  #type: ignore
        )
        return event_sent

    @staticmethod
    async def calculate_delay(scheduled_time: datetime) -> int:
        if scheduled_time < datetime.now():
            delay = 0
        else:
            delay = (scheduled_time - datetime.now()).seconds * 1000
        return delay

    @staticmethod
    async def generate_content(title: str, text: str, subject: str) -> dict:
        content = {'title': title,
                   'text': text,
                   'subject': subject}
        return content


def get_db(
        rabbitmq: AbstractQueue = Depends(get_connection),
) -> QueueHandler:
    return QueueHandler(QueueRabbit(rabbitmq))
