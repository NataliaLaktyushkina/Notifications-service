import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings

IS_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if not IS_DOCKER:
    load_dotenv()   # take environment variables from .env.


class EmailSettings(BaseSettings):
    EMAIL_USER: Optional[str]
    EMAIL_PASS: Optional[str]


class SMTPSettings(BaseSettings):
    SMTP_HOST: Optional[str]
    SMTP_PORT: Optional[str]

class Settings(BaseSettings):

    email_settings: EmailSettings = EmailSettings()
    smtp_settings: SMTPSettings = SMTPSettings()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
