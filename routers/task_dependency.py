from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import TaskDependencyBase, TaskDependencyDisplay
from db.database import get_db
from db import db_task_dependency
from typing import List
from routers.schemas import UserAuth
import uuid


router = APIRouter(
    prefix='/task-dependency',
    tags=['task-dependency']
)


@router.post('/create/{task_id_1}/links_to/{task_id_2}', response_model=TaskDependencyBase)
def create(request: TaskDependencyBase, task_id_1: uuid.UUID, task_id_2: uuid.UUID, db=Depends(get_db), current_user: UserAuth = Depends(verify_token)):
    """Create a new task Dependency."""
    return db_task_dependency.create_task_dependency(db, request, task_id_1, task_id_2, current_user)


@router.get('/all/{task_id}', response_model=List[TaskDependencyDisplay])
def all_task_Dependency(task_id: uuid.UUID, db=Depends(get_db)):
    """Retrieve all Dependencies for a specific task."""
    return db_task_dependency.get_all_task_dependency(db, task_id)


@router.delete('/delete/{dependency_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(dependency_id: uuid.UUID, db=Depends(get_db)):
    if not db_task_dependency.delete(dependency_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dependency not found")

