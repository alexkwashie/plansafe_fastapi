import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import TaskRawMaterialBase, TaskRawMaterialDisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_production_planning import db_task_raw_materials


router = APIRouter(
    prefix='/api/v1',
    tags=['task-raw-materials']
)


@router.post('/tasks/{task_id}/raw-materials', response_model=TaskRawMaterialDisplay)
async def create(request: TaskRawMaterialBase, task_id: uuid.UUID, user=Depends(get_current_user)):
    return db_task_raw_materials.create_task_raw_material(request, task_id, request.raw_material_id, user)


@router.get('/tasks/{task_id}/raw-materials')
async def list_task_raw_materials(task_id: uuid.UUID, pagination: PaginationParams = Depends()):
    data, total = db_task_raw_materials.get_all_task_raw_material(task_id, offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.delete('/task-raw-materials/{task_raw_material_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_raw_material_id: uuid.UUID, user=Depends(get_current_user)):
    """Delete a task raw material by its ID."""
    if not db_task_raw_materials.delete(task_raw_material_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task raw material not found")
