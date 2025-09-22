from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import TaskAssigneeBase, TaskAssigneeDisplay
from db.database import get_db
from db import db_task_assignee
from typing import List
from routers.schemas import UserAuth
import uuid


router = APIRouter(
    prefix='/task-assignee',
    tags=['task-assignee']
)


@router.post('/add/{task_id}/assign/{user_id}', response_model=TaskAssigneeBase)
def create(request: TaskAssigneeBase, task_id: uuid.UUID, user_id: uuid.UUID):  # Ensure user_id is a UUID
    return db_task_assignee.create_task_assignees(task_id, user_id, request)


@router.get('/all/{task_id}', response_model=List[TaskAssigneeDisplay])
def all_task_assignees(task_id: uuid.UUID):
    return db_task_assignee.get_all_task_assignee(task_id)


@router.delete('/delete/{assignee_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(task_assignee_id: uuid.UUID):
    """Delete a task assignee by its ID."""
    if not db_task_assignee.delete(task_assignee_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return {"detail": f"Assignee {task_assignee_id} deleted successfully"}
