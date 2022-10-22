"""Description of notification models."""

from datetime import datetime
from enum import Enum
from typing import Dict

from pydantic import BaseModel


class Source(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'


class EventType(str, Enum):
    welcome_letter = 'welcome_letter'
    critique_likes = 'critique_likes'
    mailing_list = 'mailing_list'


class Event(BaseModel):
    source: Source
    event_type: EventType
    scheduled_datetime: datetime
    payload: Dict


class EventSent(BaseModel):
    event_sent: bool
