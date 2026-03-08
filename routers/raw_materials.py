from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import RawMaterialBase, RawMaterialDisplay, RawMaterialUpdate
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_raw_materials import db_raw_material
import uuid


router = APIRouter(
    prefix='/api/v1/raw-materials',
    tags=['raw-materials']
)


@router.post('/', response_model=RawMaterialDisplay)
async def create(request: RawMaterialBase, user=Depends(get_current_user)):
    return db_raw_material.create_raw_material(request, user)


@router.get('/')
async def all_raw_materials(pagination: PaginationParams = Depends()):
    data, total = db_raw_material.get_all_raw_material(offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/{raw_material_id}', response_model=RawMaterialDisplay)
async def get_raw_material_by_id(raw_material_id: uuid.UUID):
    """Get a single raw material by its ID."""
    return db_raw_material.get_by_id(raw_material_id)


@router.put('/{raw_material_id}', response_model=RawMaterialDisplay)
async def update(raw_material_id: uuid.UUID, request: RawMaterialUpdate, user=Depends(get_current_user)):
    """Update a raw material by its ID."""
    return db_raw_material.update_raw_material(raw_material_id, request)


@router.delete('/{raw_material_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(raw_material_id: uuid.UUID, user=Depends(get_current_user)):
    """Delete a raw material by its ID."""
    if not db_raw_material.delete(raw_material_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raw material not found")
