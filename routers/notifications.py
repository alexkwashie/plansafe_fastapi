from fastapi import APIRouter, Depends
from dependencies.auth_token import get_current_user
from routers.schemas import NotificationDisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db import db_notifications
import uuid


router = APIRouter(
    prefix='/api/v1',
    tags=['notifications']
)


@router.get('/notifications')
async def list_notifications(pagination: PaginationParams = Depends(), user=Depends(get_current_user)):
    """List notifications for the current user (paginated)."""
    user_id = user.get("user_id") if isinstance(user, dict) else str(user)
    data, total = db_notifications.get_notifications_for_user(user_id, offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.put('/notifications/{notification_id}/read', response_model=NotificationDisplay)
async def mark_read(notification_id: uuid.UUID, user=Depends(get_current_user)):
    """Mark a notification as read."""
    return db_notifications.mark_as_read(notification_id)
