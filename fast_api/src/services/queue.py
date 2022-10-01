import abc
from models.notifications import NotificationSent


class AbstractQueue(abc.ABC):

    @abc.abstractmethod
    async def publish(self, movie_id: str, user_id: str) -> NotificationSent:
        pass


class QueueRabbit(AbstractQueue):

    def __init__(self, client: Rabbit):
        self.client = client

    async def publish(self, movie_id: str, user_id: str) -> NotificationSent:
        return NotificationSent(notificaton_sent=True)
