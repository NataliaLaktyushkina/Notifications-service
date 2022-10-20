import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings

IS_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if not IS_DOCKER:
    load_dotenv()   # take environment variables from .env.


class Settings(BaseSettings):

    MOVIES_NUMBER: Optional[int]
    USERS_NUMBER: Optional[int]
    SCHEDULE: Optional[int]
    HOUR: Optional[str]
    MINUTE: Optional[str]
    AUTH_SERVICE: Optional[str]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
