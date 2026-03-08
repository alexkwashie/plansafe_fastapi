from fastapi import APIRouter, Depends
from routers.schemas import UserDisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db import db_user
import uuid


router = APIRouter(
    prefix='/api/v1/users',
    tags=['users']
)


@router.get('/')
async def all_users(pagination: PaginationParams = Depends()):
    data, total = db_user.get_all_users(offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/{user_id}', response_model=UserDisplay)
async def get_user_by_id(user_id: uuid.UUID):
    """Get user by their ID."""
    return db_user.get_current_user(user_id)
