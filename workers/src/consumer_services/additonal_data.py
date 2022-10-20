from typing import Dict, List, Union


def additional_info_for_email(routing_key: str,
                              user: dict,
                              content: List) -> dict:
    add_data: Dict[str, Union[List[str], str]] = {}
    if routing_key == 'registration':
        add_data['receivers'] = [user['email']]
        add_data['subject'] = f'Registration update for {user["name"]}'
        add_data['title'] = 'Registration complete'
        add_data['template'] = 'mail.html'
        add_data['text'] = 'Thanks for registration'
    elif routing_key == 'celery':
        add_data['receivers'] = [user['email']]
        add_data['subject'] = f'Likes update for {user["name"]}'
        add_data['title'] = 'Since last time you received likes for next movies:'
        add_data['template'] = 'likes.html'
        add_data['text'] = ''
        for movie in content:
            movie: dict  # type: ignore
            add_data['text'] = '\n'.join([add_data['text'], ':'.join([movie['movie_id'],  # type: ignore
                                                                      str(movie['likes'])])])

    return add_data
