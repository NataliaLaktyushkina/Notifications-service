from models.events import Event, Source, EventType
from datetime import datetime
from core.config import settings
import uuid
from random import randint

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
        for _j in range(randint(1,MOVIES_NUMBER)):  # noqa: S311
            movie_id = uuid.uuid4()
            n_likes = randint(1, 10)  # noqa: S311
            content.append(
                {'movie_id': movie_id,
                 'likes': n_likes,
                 },
             )
        users_list.append({'user':
                       {'user_id': user_id },
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


def main() -> None:
    event = generate_event()
    print(event)
    # put_events_to_queue(events_list)   # noqa: E800


if __name__ == '__main__':
    main()
