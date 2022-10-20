import json
import os
import sys
import uuid
from datetime import datetime
from random import randint

from celery import Celery
from celery.schedules import crontab

sys.path.append(os.path.dirname(__file__) + '/..')

from consumer_services.generate_email import generate_email  # noqa: E402
from worker_models.events import Event, EventType, Source   # noqa: E402
from settings.common.config import settings   # noqa: E402
from settings.rabbitmq.config import rabbit_settings   # noqa: E402

# broker_url = 'amqp://my_user:my_pass@127.0.0.1:5672'  # noqa: E800
USER = rabbit_settings.rabbitmq_settings.RABBITMQ_USER
PASS = rabbit_settings.rabbitmq_settings.RABBITMQ_PASS
HOST = rabbit_settings.rabbitmq_settings.RABBITMQ_HOST
PORT = rabbit_settings.rabbitmq_settings.RABBITMQ_PORT
broker_url = f'amqp://{USER}:{PASS}@{HOST}:{PORT}'
app = Celery('generator', broker=broker_url)

app.conf.beat_schedule = {
    'run-me-every-ten-seconds': {
        'task': 'generator.generate_event',
        'schedule': crontab(minute=settings.MINUTE),
    },
}

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


@app.task
def generate_event() -> None:
    source = Source.email
    event_type = EventType.likes_number
    scheduled_time = datetime.now()
    payload = get_payload_likes()
    event = Event(source=source,
                  event_type=event_type,
                  scheduled_datetime=scheduled_time,
                  payload=payload,
                  )
    generate_email('celery', json.loads(event.json()))


if __name__ == '__main__':
    generate_event()
