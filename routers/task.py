from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import TaskBase, TaskDisplay, TaskUpdateBase
from db.database import get_db
from db import db_task
from typing import List
from routers.schemas import UserAuth
import uuid


router = APIRouter(
    prefix='/task',
    tags=['task']
)


@router.post('/create-task/{batch_id}', response_model=TaskDisplay)
def create(request: TaskBase, batch_id: uuid.UUID):
    return db_task.create_task(request, batch_id)


@router.get('/all/{batch_id}', response_model=List[TaskDisplay])
def all_task(batch_id: uuid.UUID):
    return db_task.get_all_task(batch_id)

@router.put('/update/{id}', response_model=TaskDisplay)
def update(task_id: uuid.UUID, request: TaskUpdateBase):
    """Update a task by its ID."""
    return db_task.update_task(task_id, request)

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: uuid.UUID):
    """Delete a task raw materials by its ID."""
    if not db_task.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Related Task not found")
    return {"detail": f"Task with id:{id} deleted successfully"}
