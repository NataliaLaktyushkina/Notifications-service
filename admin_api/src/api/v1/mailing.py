"""Endpoints of users API."""

from datetime import datetime
from fastapi import APIRouter, Depends, Query
from services.mailing import get_db, QueueHandler

from models.events import EventSent

router = APIRouter()


@router.post('/', description='Create new mailing',
             response_description='Mailing created',
             )
async def create_mailing(
        title: str,
        text: str,
        subject: str,
        receivers: list[str] = Query(default=[]),  # type: ignore
        scheduled_time: datetime = Query(default=datetime.now()),
        service: QueueHandler = Depends(get_db),
) -> EventSent:
    """Send letters to users."""
    content = await service.generate_content(title, text, subject)
    return await service.send_notification(
        content, receivers, scheduled_time,
    )
