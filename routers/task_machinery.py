from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import TaskMachineryBase, TaskMachineryDisplay
from db.database import get_db
from db import db_task_machinery
from typing import List
from routers.schemas import UserAuth
import uuid


router = APIRouter(
    prefix='/task-machinery',
    tags=['task-machinery']
)


@router.post('/add/{task_id}/machinery/{machinery_id}', response_model=TaskMachineryBase)
def create(request: TaskMachineryBase, task_id: uuid.UUID, machinery_id: uuid.UUID, db=Depends(get_db), user=Depends(verify_token)):
    return db_task_machinery.create_task_machinery(request, task_id, machinery_id ,user)


@router.get('/all/{task_id}', response_model=List[TaskMachineryDisplay])
def all_task_assignees(task_id: uuid.UUID, db=Depends(get_db)):
    return db_task_machinery.get_all_task_machinery(db, task_id)


@router.delete('/delete/{task_machinery_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(task_machinery_id: uuid.UUID, db=Depends(get_db)):
    """Delete a task machinery by its ID."""
    if not db_task_machinery.delete(task_machinery_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return {"detail": f"Assignee {task_machinery_id} deleted successfully"}



