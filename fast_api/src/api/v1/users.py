"""Endpoints of users API"""

from fastapi import APIRouter, Depends
from models.events import EventSent
from services.jwt_check import JWTBearer
from services.users import get_db, QueueHandler

router = APIRouter()


@router.post('/', description='New user',
             response_description='User registration',
             )
async def user_registration(
        user_id: str = Depends(JWTBearer()),
        service: QueueHandler = Depends(get_db),
) -> EventSent:
    """Send welcome letter to user."""
    return await service.send_notification(user_id=user_id)
