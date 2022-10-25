from typing import Dict, List, Union
from consumer_services.db_data import get_template_by_key  # noqa: E800
from worker_models.events import Templates


def additional_info_for_email(routing_key: str,
                              user: dict,
                              content: dict) -> dict:
    add_data: Dict[str, Union[List[str], str, Templates]] = {}
    add_data['template'] = get_template_by_key(routing_key)  # noqa: E800
    if routing_key == 'registration':
        add_data['receivers'] = [user['email']]
        add_data['subject'] = f'Registration update for {user["name"]}'
        add_data['title'] = 'Registration complete'
        add_data['text'] = 'Thanks for registration'
    elif routing_key == 'celery':
        add_data['receivers'] = [user['email']]
        add_data['subject'] = f'Likes update for {user["name"]}'
        add_data['title'] = 'Since last time you received likes for next movies:'
        add_data['text'] = ''
        for movie in content:
            movie: dict  # type: ignore
            add_data['text'] = '\n'.join([add_data['text'], ':'.join([movie['movie_id'],  # type: ignore
                                                                      str(movie['likes'])])])
    elif routing_key == 'admin_mailing':
        add_data['receivers'] = [user['email']]
        add_data['subject'] = content['subject']
        add_data['title'] = content['title']
        add_data['text'] = content['text']
    return add_data
