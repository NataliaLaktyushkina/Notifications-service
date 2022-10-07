"""Description of notification models."""

from models.json_config import BaseOrjsonModel


class NotificationSent(BaseOrjsonModel):
    """This is the description of critique post response  model."""

    notification_sent: bool
