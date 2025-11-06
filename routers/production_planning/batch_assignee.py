from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import BatchAssigneeBase, BatchAssigneeDisplay
from db.db_production_planning import db_batch_assignee
from typing import List
from routers.schemas import UserAuth
import uuid


router = APIRouter(
    prefix='/batch-assignee',
    tags=['batch-assignee']
)


@router.post('/add/{batch_id}/assign/{user_id}', response_model=BatchAssigneeBase)
def create(request: BatchAssigneeBase, batch_id: uuid.UUID, user_id: uuid.UUID):  # Ensure user_id is a UUID
    return db_batch_assignee.create_batch_assignees(batch_id, user_id, request)


@router.get('/all/{batch_id}', response_model=List[BatchAssigneeDisplay])
def all_task_assignees(batch_id: uuid.UUID):
    return db_batch_assignee.get_all_batch_assignee(batch_id)


@router.delete('/delete/{assignee_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(batch_assignee_id: uuid.UUID):
    """Delete a task assignee by its ID."""
    if not db_batch_assignee.delete(batch_assignee_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return {"detail": f"Assignee {batch_assignee_id} deleted successfully"}
