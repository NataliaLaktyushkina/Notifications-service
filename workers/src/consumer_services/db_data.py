from worker_models.events import Templates
from postgres_db import SessionLocal
from typing import Union


def get_template_by_key(key: str) -> Union[Templates, None]:
    service = SessionLocal()
    template = service.query(Templates).filter_by(name=key).first()
    return template


if __name__ == '__main__':
    get_template_by_key('welcome_letter')
