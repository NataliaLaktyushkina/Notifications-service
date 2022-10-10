import asyncio
import uuid
from datetime import datetime
from random import randint

import backoff
import pika

from core.config import settings
from db import queue_rabbit
from schedul_models.events import Event, Source, EventType, EventSent
from schedul_services.events import QueueHandler
from schedul_services.scheduler_queue import QueueRabbit

USERS_NUMBER = settings.USERS_NUMBER
MOVIES_NUMBER = settings.MOVIES_NUMBER


def get_payload_likes() -> dict:
    # Для каждого пользователя свой список фильмов и рецензий к ним
    # payload - {users:
    #               [{user : {user_id : user_id_1},
    #                 content: {movie: n, movie_2: n2}   # noqa: E800
    #                   },

    #                {user: {user_id: user_id_2},
    #                  content: {movie: n, movie_2: n2}   # noqa: E800
    #                   }   # noqa: E800
    #               ]}   # noqa: E800
    users_list = []

    for _i in range(USERS_NUMBER):

        user_id = uuid.uuid4()
        content = []
        for _j in range(randint(1, MOVIES_NUMBER)):  # noqa: S311
            movie_id = uuid.uuid4()
            n_likes = randint(1, 10)  # noqa: S311
            content.append(
                {'movie_id': movie_id,
                 'likes': n_likes,
                 },
            )
        users_list.append({'user':
                               {'user_id': user_id},
                           'content': content,
                           })
    payload = {'users': users_list}
    return payload


def generate_event() -> Event:
    source = Source.email
    event_type = EventType.likes_number
    scheduled_time = datetime(2022, 10, 9, 22, 30)
    payload = get_payload_likes()
    return Event(source=source,
                 event_type=event_type,
                 scheduled_datetime=scheduled_time,
                 payload=payload,
                 )


async def put_event_to_queue(
        event: Event,
        service: QueueHandler) -> EventSent:
    return await service.send_event(event)


async def startup() -> None:
    """Start up settings - connect to RabbitMQ"""

    rabbitmq_settings = settings.rabbitmq_settings

    credentials = pika.PlainCredentials(
        rabbitmq_settings.RABBITMQ_USER,
        rabbitmq_settings.RABBITMQ_PASS,
    )
    parameters = pika.ConnectionParameters(
        host=rabbitmq_settings.RABBITMQ_HOST,
        port=rabbitmq_settings.RABBITMQ_PORT,
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300,
    )

    @backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError)
    def _connect() -> pika.BlockingConnection:
        return pika.BlockingConnection(parameters=parameters)

    queue_rabbit.connection = _connect()


async def main() -> EventSent:
    await startup()
    rabbitmq = await queue_rabbit.get_connection()
    event = generate_event()
    return await put_event_to_queue(event, QueueHandler(QueueRabbit(rabbitmq)))


if __name__ == '__main__':
    asyncio.run(main())
