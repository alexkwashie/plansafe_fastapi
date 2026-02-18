import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import TaskBase, TaskDisplay, TaskUpdateBase
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_production_planning import db_task


router = APIRouter(
    prefix='/api/v1',
    tags=['tasks']
)


@router.post('/batches/{batch_id}/tasks', response_model=TaskDisplay)
async def create(request: TaskBase, batch_id: uuid.UUID, user=Depends(get_current_user)):
    return db_task.create_task(request, batch_id)


@router.get('/batches/{batch_id}/tasks')
async def list_tasks(batch_id: uuid.UUID, pagination: PaginationParams = Depends()):
    data, total = db_task.get_all_task(batch_id, offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/tasks/{task_id}', response_model=TaskDisplay)
async def get_task(task_id: uuid.UUID):
    return db_task.get_by_id(task_id)


@router.put('/tasks/{task_id}', response_model=TaskDisplay)
async def update(task_id: uuid.UUID, request: TaskUpdateBase, user=Depends(get_current_user)):
    """Update a task by its ID."""
    return db_task.update_task(task_id, request)


@router.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_id: uuid.UUID, user=Depends(get_current_user)):
    """Delete a task by its ID."""
    if not db_task.delete(task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
