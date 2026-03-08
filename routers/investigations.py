from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import InvestigationBase, InvestigationUpdate, InvestigationDisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_investigations import db_investigation
import uuid


router = APIRouter(
    prefix='/api/v1',
    tags=['investigations']
)


@router.post('/incidents/{incident_id}/investigations', response_model=InvestigationDisplay)
async def create(incident_id: uuid.UUID, request: InvestigationBase, user=Depends(get_current_user)):
    return db_investigation.create_investigation(incident_id, request, user)


@router.get('/incidents/{incident_id}/investigations')
async def list_investigations(incident_id: uuid.UUID, pagination: PaginationParams = Depends()):
    data, total = db_investigation.get_investigations_for_incident(incident_id, offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/investigations/{investigation_id}', response_model=InvestigationDisplay)
async def get_investigation(investigation_id: uuid.UUID):
    return db_investigation.get_by_id(investigation_id)


@router.put('/investigations/{investigation_id}', response_model=InvestigationDisplay)
async def update(investigation_id: uuid.UUID, request: InvestigationUpdate, user=Depends(get_current_user)):
    return db_investigation.update_investigation(investigation_id, request, user)
