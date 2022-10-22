"""Endpoints of users API"""

from fastapi import APIRouter, Depends
from models.events import EventSent
from services.mailing import get_db, QueueHandler

router = APIRouter()


@router.post('/', description='Create new mailing',
             response_description='Mailing created',
             )
async def create_mailing(
        title: str,
        text: str,
        subject: str,
        receivers: list[str],  # type: ignore
        service: QueueHandler = Depends(get_db),
) -> EventSent:
    """Send letters to users."""
    return await service.send_notification(
        title, text, subject, receivers)
