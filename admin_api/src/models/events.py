"""Description of notification models."""

from enum import Enum
from typing import List

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
    payload: List


class EventSent(BaseModel):
    event_sent: bool
