from fastapi import Depends
from services.service_bookmark import AbstractQueue, QueueRabbit
from models.notifications import NotificationSent


class QueueHandler:
    def __init__(self, queue: AbstractQueue):
        self.queue = queue

    async def publish(self, movie_id: str, user_id: str) -> NotificationSent:
        bookmark_added = await self.bookmark_db.add_bookmark(movie_id, user_id)
        return BookmarkAdded(added=bookmark_added)


def get_db(
        RabbitMQ: AbstractQueue = Depends(get_rabbit),
) -> RabbitHandler:
    return QueueHandler(QueueRabbit(RabbitMQ))
