from models.events import Event, Source, EventType
from datetime import datetime
from core.config import settings
import uuid
from random import randint

NUMBER_EVENTS = settings.NUMBER_EVENTS


def get_payload_likes() -> dict:
    user_id = uuid.uuid4()
    movie_id = uuid.uuid4()
    n_likes = randint(1, 10)  # noqa: S311
    payload = {'user':
                   {'user_id': user_id },
               'content': [
                   {'movie_id': movie_id,
                    'likes': n_likes,
                    },
               ],
               }
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


def main() -> list:
    events_list = []
    for _i in range(NUMBER_EVENTS):
        event = generate_event()
        events_list.append(event)
    print(events_list)
    return events_list


if __name__ == '__main__':
    main()
