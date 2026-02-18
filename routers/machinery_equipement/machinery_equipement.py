import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import MachineryDisplay, MachineryBase, MachineryBaseUpdate
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_machinery_equipement import db_machinery_equipement


router = APIRouter(
    prefix='/api/v1/machinery',
    tags=['machinery']
)


@router.post('/', response_model=MachineryDisplay)
async def create(request: MachineryBase, user=Depends(get_current_user)):
    return db_machinery_equipement.create_machinery(request, user)


@router.get('/')
async def all_machinery(pagination: PaginationParams = Depends()):
    data, total = db_machinery_equipement.get_all_machinery(offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/{machinery_id}', response_model=MachineryDisplay)
async def get_machinery_by_id(machinery_id: uuid.UUID):
    """Get a single machinery record by its ID."""
    return db_machinery_equipement.get_by_id(machinery_id)


@router.put('/{machinery_id}', response_model=MachineryDisplay)
async def update(machinery_id: uuid.UUID, request: MachineryBaseUpdate, user=Depends(get_current_user)):
    """Update a machinery by its ID."""
    return db_machinery_equipement.update_machinery(machinery_id, request)


@router.delete('/{machinery_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(machinery_id: uuid.UUID, user=Depends(get_current_user)):
    """Delete a machinery by its ID."""
    if not db_machinery_equipement.delete(machinery_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machinery not found")
