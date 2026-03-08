import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import BatchBase, BatchDisplay, BatchBaseUpdate
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_production_planning import db_batch


router = APIRouter(
    prefix='/api/v1/batches',
    tags=['batches']
)


@router.post('/', response_model=BatchDisplay)
async def create(request: BatchBase, user=Depends(get_current_user)):
    return db_batch.create_batch(request, user)


@router.get('/')
async def list_batches(pagination: PaginationParams = Depends()):
    data, total = db_batch.get_all(offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/{batch_id}', response_model=BatchDisplay)
async def get_batch(batch_id: uuid.UUID):
    return db_batch.get_by_id(batch_id)


@router.put('/{batch_id}', response_model=BatchDisplay)
async def update(batch_id: uuid.UUID, request: BatchBaseUpdate, user=Depends(get_current_user)):
    """Update a batch by its ID."""
    return db_batch.update_batch(batch_id, request)


@router.delete('/{batch_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(batch_id: uuid.UUID, user=Depends(get_current_user)):
    """Delete a batch by its ID."""
    if not db_batch.delete(batch_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
