import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import TaskMachineryBase, TaskMachineryDisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_production_planning import db_task_machinery


router = APIRouter(
    prefix='/api/v1',
    tags=['task-machinery']
)


@router.post('/tasks/{task_id}/machinery', response_model=TaskMachineryDisplay)
async def create(request: TaskMachineryBase, task_id: uuid.UUID, user=Depends(get_current_user)):
    return db_task_machinery.create_task_machinery(request, task_id, request.machinery_id, user)


@router.get('/tasks/{task_id}/machinery')
async def list_task_machinery(task_id: uuid.UUID, pagination: PaginationParams = Depends()):
    data, total = db_task_machinery.get_all_task_machinery(task_id, offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.delete('/task-machinery/{task_machinery_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_machinery_id: uuid.UUID, user=Depends(get_current_user)):
    """Delete a task machinery by its ID."""
    if not db_task_machinery.delete(task_machinery_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task machinery not found")
