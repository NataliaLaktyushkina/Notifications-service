from datetime import datetime

from fastapi import Depends

from db.queue_rabbit import get_connection
from models.events import EventSent, EventType
from services.queue import AbstractQueue, QueueRabbit


class QueueHandler:
    def __init__(self, queue: AbstractQueue):
        self.queue = queue

    async def send_notification(
            self, payload: list, event_type: EventType,
            scheduled_time: datetime,
        ) -> EventSent:
        event_sent = await self.queue.send_msg(
            payload, event_type, scheduled_time,
        )
        return event_sent

    @staticmethod
    async def payload_user_registration(user_id: str) -> list:
        receivers = [user_id]
        content = [{'user_id': user_id }]
        payload = [{'users': receivers,
                   'content': content}]
        return payload


def get_db(
        rabbitmq: AbstractQueue = Depends(get_connection),
) -> QueueHandler:
    return QueueHandler(QueueRabbit(rabbitmq))
