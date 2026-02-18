import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import BatchAssigneeBase, BatchAssigneeDisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_production_planning import db_batch_assignee


router = APIRouter(
    prefix='/api/v1',
    tags=['batch-assignees']
)


@router.post('/batches/{batch_id}/assignees', response_model=BatchAssigneeDisplay)
async def create(request: BatchAssigneeBase, batch_id: uuid.UUID, user=Depends(get_current_user)):
    return db_batch_assignee.create_batch_assignees(batch_id, request.user_id, request)


@router.get('/batches/{batch_id}/assignees')
async def list_batch_assignees(batch_id: uuid.UUID, pagination: PaginationParams = Depends()):
    data, total = db_batch_assignee.get_all_batch_assignee(batch_id, offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.delete('/batch-assignees/{assignee_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(assignee_id: uuid.UUID, user=Depends(get_current_user)):
    """Delete a batch assignee by its ID."""
    if not db_batch_assignee.delete(assignee_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch assignee not found")
