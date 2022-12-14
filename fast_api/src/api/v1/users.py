"""Endpoints of users API"""

from fastapi import APIRouter, Depends
from models.events import EventSent, EventType
from services.jwt_check import JWTBearer
from services.users import get_db, QueueHandler
from datetime import datetime

router = APIRouter()


@router.post('/', description='New user',
             response_description='User registration',
             )
async def user_registration(
        user_id: str = Depends(JWTBearer()),
        service: QueueHandler = Depends(get_db),
) -> EventSent:
    """Send welcome letter to user."""
    payload = await service.payload_user_registration(user_id=user_id)
    return await service.send_notification(
        payload,
        event_type=EventType.welcome_letter,
        scheduled_time=datetime.now(),
    )
