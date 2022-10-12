from typing import Dict, List, Union


def additional_info_for_email(routing_key: str) -> dict:
    add_data: Dict[str, Union[List[str], str]] = {}
    if routing_key == 'registration':
        add_data['receivers'] = ['education_tests@mail.ru']
        add_data['subject'] = 'Registration confirmation'
        add_data['title'] = 'Registration complete'
        add_data['template'] = 'mail.html'
        add_data['text'] = 'Thanks for registration'
    elif routing_key == 'likes':
        add_data['receivers'] = ['education_tests@mail.ru']
        add_data['subject'] = 'Likes update'
        add_data['title'] = 'Since last time you recieved likes'
        add_data['template'] = 'mail.html'
        add_data['text'] = 'Keep it up!'
    return add_data
