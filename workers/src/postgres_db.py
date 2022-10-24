"""Модуль содержит вспомогательный функции для работы с базой данных."""
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings.postgres import config

db_settings = config.settings

username = db_settings.USERNAME
password = db_settings.PASSWORD
host = db_settings.HOST
port = db_settings.PORT
host_port = ':'.join((host, port))
database_name = db_settings.DATABASE_NAME

SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{host_port}/{database_name}'


logger = logging.getLogger(__name__)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
