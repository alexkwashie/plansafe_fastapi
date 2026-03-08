from fastapi import APIRouter, Depends, Query
from dependencies.auth_token import get_current_user
from routers.schemas import (
    InspectionBase, InspectionUpdate, InspectionDisplay,
    InspectionResponseBase, InspectionResponseDisplay,
)
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_checklists import db_inspection
import uuid
from typing import Optional


router = APIRouter(
    prefix='/api/v1',
    tags=['inspections']
)


@router.post('/inspections', response_model=InspectionDisplay)
async def create(request: InspectionBase, user=Depends(get_current_user)):
    return db_inspection.create_inspection(request, user)


@router.get('/inspections')
async def list_inspections(
    pagination: PaginationParams = Depends(),
    status: Optional[str] = Query(None, description="Filter by status"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
):
    data, total = db_inspection.get_all_inspections(
        offset=pagination.offset,
        limit=pagination.limit,
        status_filter=status,
        date_from=date_from,
        date_to=date_to,
    )
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/inspections/{inspection_id}')
async def get_inspection(inspection_id: uuid.UUID):
    """Get inspection with all responses."""
    return db_inspection.get_with_responses(inspection_id)


@router.put('/inspections/{inspection_id}', response_model=InspectionDisplay)
async def update(inspection_id: uuid.UUID, request: InspectionUpdate, user=Depends(get_current_user)):
    return db_inspection.update_inspection(inspection_id, request, user)


@router.post('/inspections/{inspection_id}/responses', response_model=InspectionResponseDisplay)
async def submit_response(inspection_id: uuid.UUID, request: InspectionResponseBase, user=Depends(get_current_user)):
    """Submit a checklist response. Failed items auto-create follow-up tasks."""
    return db_inspection.submit_response(inspection_id, request)
