"""Description of notification models."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from postgres_db import Base


class Source(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'


class EventType(str, Enum):
    welcome_letter = 'welcome_letter'
    likes_number = 'likes_number'


class Event(BaseModel):
    source: Source
    event_type: EventType
    scheduled_datetime: datetime
    payload: list


class EventSent(BaseModel):
    event_sent: bool


class Templates(Base):
    __tablename__ = 'templates'

    id = Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    html = Column(Text, nullable=False)
