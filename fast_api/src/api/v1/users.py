"""Endpoints of users API"""

from fastapi import APIRouter, Depends
from models.notifications import NotificationSent
from services.jwt_check import JWTBearer

router = APIRouter()


@router.post('/', description='New user',
            response_description='User registration',
            )
async def user_registration(
        user_id: str = Depends(JWTBearer()),
) -> NotificationSent:
    """Send welcome letter to user."""
    pass
    # return await service.sent_notification(user_id=user_id)
