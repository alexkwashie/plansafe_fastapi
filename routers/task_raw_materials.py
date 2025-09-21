from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import TaskRawMaterialBase, TaskRawMaterialDisplay
from db.database import get_db
from db import db_task_raw_materials
from typing import List
from routers.schemas import UserAuth
import uuid


router = APIRouter(
    prefix='/task-raw-materials',
    tags=['task-raw-materials']
)


@router.post('/create/{task_id}', response_model=TaskRawMaterialBase)
def create(request: TaskRawMaterialBase, task_id: uuid.UUID, db=Depends(get_db), current_user: UserAuth = Depends(verify_token)):
    return db_task_raw_materials.create_task_raw_material(db, request, task_id, current_user)


@router.get('/all/{task_id}', response_model=List[TaskRawMaterialDisplay])
def all_task_raw_materials(task_id: uuid.UUID, db=Depends(get_db)):
    return db_task_raw_materials.get_all_task_raw_material(db, task_id)


@router.delete('/delete/{task_raw_material_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(task_raw_material_id: uuid.UUID, db=Depends(get_db)):
    """Delete a task raw materials by its ID."""
    if not db_task_raw_materials.delete(task_raw_material_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task raw material not found")
    return {"detail": f"Task Raw Materials {task_raw_material_id} deleted successfully"}



