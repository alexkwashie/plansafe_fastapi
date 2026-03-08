from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import CAPABase, CAPAUpdate, CAPADisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_investigations import db_capa
import uuid


router = APIRouter(
    prefix='/api/v1',
    tags=['capa-actions']
)


@router.post('/investigations/{investigation_id}/capa-actions', response_model=CAPADisplay)
async def create(investigation_id: uuid.UUID, request: CAPABase, user=Depends(get_current_user)):
    return db_capa.create_capa(investigation_id, request, user)


@router.get('/investigations/{investigation_id}/capa-actions')
async def list_capas(investigation_id: uuid.UUID, pagination: PaginationParams = Depends()):
    data, total = db_capa.get_capas_for_investigation(investigation_id, offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/capa-actions/{capa_id}', response_model=CAPADisplay)
async def get_capa(capa_id: uuid.UUID):
    return db_capa.get_by_id(capa_id)


@router.put('/capa-actions/{capa_id}', response_model=CAPADisplay)
async def update(capa_id: uuid.UUID, request: CAPAUpdate, user=Depends(get_current_user)):
    return db_capa.update_capa(capa_id, request, user)


@router.delete('/capa-actions/{capa_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(capa_id: uuid.UUID, user=Depends(get_current_user)):
    if not db_capa.delete_capa(capa_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CAPA action not found")
