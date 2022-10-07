import os
from typing import Optional, Union

from dotenv import load_dotenv
from pydantic import BaseSettings

IS_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if not IS_DOCKER:
    load_dotenv()   # take environment variables from .env.


class RabbitMQUser(BaseSettings):
    """RabbitMQ username and password"""

    RABBITMQ_USER: Optional[str] = os.getenv('RABBITMQ_DEFAULT_USER')
    RABBITMQ_PASS: Optional[str] = os.getenv('RABBITMQ_DEFAULT_PASS')  # noqa: WPS115

    RABBITMQ_EXCHANGE: Optional[str]
    RABBITMQ_EXCHANGE_TYPE: Optional[str]
    RABBITMQ_QUEUE_NAME: Optional[str]


class RabbitMQSettingsProm(RabbitMQUser):
    """ RABBITMQ host and port for production"""

    RABBITMQ_HOST: Optional[str]
    RABBITMQ_PORT: Optional[str]


class RabbitMQSettingsDev(RabbitMQUser):
    """ RABBITMQ host and port for development"""

    RABBITMQ_HOST: Optional[str] = os.getenv('RABBITMQ_HOST_DEBUG')  # noqa: WPS115
    RABBITMQ_PORT: Optional[str] = os.getenv('RABBITMQ_PORT_DEBUG')  # noqa: WPS115


class Settings(BaseSettings):

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


class PromSettings(Settings):
    rabbitmq_settings: RabbitMQSettingsProm = RabbitMQSettingsProm()


class DevSettings(Settings):
    rabbitmq_settings: RabbitMQSettingsDev = RabbitMQSettingsDev()


def get_settings() -> Union[PromSettings, DevSettings]:
    environment = os.getenv('ENVIRONMENT')
    if environment == 'prom':
        return PromSettings()
    return DevSettings()


rabbit_settings = get_settings()
