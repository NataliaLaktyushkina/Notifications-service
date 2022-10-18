from typing import Dict, List, Union


def additional_info_for_email(routing_key: str,
                              user: str,
                              content: List) -> dict:
    add_data: Dict[str, Union[List[str], str]] = {}
    if routing_key == 'registration':
        add_data['receivers'] = ['education_tests@mail.ru']
        add_data['subject'] = f'Celery update {user}'
        add_data['title'] = 'Registration complete'
        add_data['template'] = 'mail.html'
        add_data['text'] = 'Thanks for registration'
    elif routing_key == 'celery':
        add_data['receivers'] = ['education_tests@mail.ru']
        add_data['subject'] = f'Registration confirmation for user {user}'
        add_data['title'] = 'Registration complete'
        add_data['template'] = 'mail.html'
        add_data['text'] = 'Celery info'

    elif routing_key == 'likes' :
        add_data['receivers'] = ['education_tests@mail.ru']
        add_data['subject'] = f'Likes update for {user}'
        add_data['title'] = 'Since last time you received likes for next movies:'
        add_data['template'] = 'likes.html'
        add_data['text'] = ''
        for movie in content:
            movie: dict = movie
            add_data['text'] = '\n'.join([add_data['text'], ':'.join([movie['movie_id'],
                                                                      str(movie['likes'])])])
    return add_data
