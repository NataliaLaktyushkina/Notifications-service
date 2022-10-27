from datetime import datetime
from typing import Dict

from fastapi import Depends

from db.queue_rabbit import get_connection
from models.events import EventSent, EventType
from services.queue import AbstractQueue, QueueRabbit


class QueueHandler:
    def __init__(self, queue: AbstractQueue):
        self.queue = queue

    async def send_notification(
            self, payload: Dict, event_type: EventType,
            scheduled_time: datetime,
        ) -> EventSent:
        event_sent = await self.queue.send_msg(
            payload, event_type, scheduled_time,
        )
        return event_sent

    @staticmethod
    async def payload_user_registration(user_id: str) -> Dict:
        content = [{'user_id': user_id,
                    }]
        users_list = [{'user':
                           {'user_id': user_id},
                       'content': content,
                       }]

        payload = {'users': users_list}
        return payload


def get_db(
        rabbitmq: AbstractQueue = Depends(get_connection),
) -> QueueHandler:
    return QueueHandler(QueueRabbit(rabbitmq))
