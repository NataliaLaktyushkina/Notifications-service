"""Description of notification models."""

from datetime import datetime
from enum import Enum
from typing import Dict

from pydantic import BaseModel

from models.json_config import BaseOrjsonModel


class NotificationSent(BaseOrjsonModel):
    """This is the description of critique post response  model."""

    notification_sent: bool


class Source(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'


class EventType(str, Enum):
    welcome_letter = 'welcome_letter'
    critique_likes = 'critique_likes'


class Event(BaseModel):
    source: Source
    event_type: EventType
    scheduled_datetime: datetime
    payload: Dict
