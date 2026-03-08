from fastapi import APIRouter, Depends, Query
from dependencies.auth_token import get_current_user
from routers.schemas import ShiftHandoverBase, ShiftHandoverDisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db import db_shift_handovers
import uuid
from typing import Optional


router = APIRouter(
    prefix='/api/v1',
    tags=['shift-handovers']
)


@router.post('/shift-handovers', response_model=ShiftHandoverDisplay)
async def create(request: ShiftHandoverBase, user=Depends(get_current_user)):
    return db_shift_handovers.create_handover(request, user)


@router.get('/shift-handovers')
async def list_handovers(
    pagination: PaginationParams = Depends(),
    date: Optional[str] = Query(None, description="Filter by shift date (YYYY-MM-DD)"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
):
    data, total = db_shift_handovers.get_all_handovers(
        offset=pagination.offset,
        limit=pagination.limit,
        date_filter=date,
        user_filter=user_id,
    )
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/shift-handovers/{handover_id}', response_model=ShiftHandoverDisplay)
async def get_handover(handover_id: uuid.UUID):
    return db_shift_handovers.get_by_id(handover_id)


@router.put('/shift-handovers/{handover_id}/acknowledge', response_model=ShiftHandoverDisplay)
async def acknowledge(handover_id: uuid.UUID, user=Depends(get_current_user)):
    """Incoming user acknowledges the shift handover."""
    return db_shift_handovers.acknowledge_handover(handover_id, user)
