import json
import os
import sys
import uuid
from datetime import datetime
from random import randint

from celery import Celery

sys.path.append(os.path.dirname(__file__) + '/..')

from consumer_services.generate_email import generate_email
from worker_models.events import Event, EventSent, EventType, Source

broker_url = 'amqp://my_user:my_pass@127.0.0.1:5672'
app = Celery('generator', broker=broker_url)

app.conf.beat_schedule = {
    "run-me-every-ten-seconds": {
        "task": "generator.generate_event",
        "schedule": 10.0
    }
}

USERS_NUMBER = 10
MOVIES_NUMBER = 5


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
    event_j = event.json()
    generate_email('celery', json.loads(event_j))
    # return event.json()
    # return  put_event_to_queue(event, QueueHandler(QueueRabbit(rabbitmq)))

    # return Event(source=source,
    #              event_type=event_type,
    #              scheduled_datetime=scheduled_time,
    #              payload=payload,
    #              )


if __name__ == '__main__':
    generate_event()
    # asyncio.run(main())
