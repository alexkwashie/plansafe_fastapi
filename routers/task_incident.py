from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import TaskIncidentBase, TaskIncidentDisplay
from db.database import get_db
from db import db_task_incident
from typing import List
from routers.schemas import UserAuth
import uuid


router = APIRouter(
    prefix='/task-incident',
    tags=['task-incident']
)


@router.post('/create/{task_id}', response_model=TaskIncidentBase)
def create(request: TaskIncidentBase, task_id: uuid.UUID, db=Depends(get_db), current_user: UserAuth = Depends(verify_token)):
    """Create a new task Incident."""
    return db_task_incident.create_task_dependency(db, request, task_id, current_user)


@router.get('/all/{task_id}', response_model=List[TaskIncidentDisplay])
def all_task_Dependencys(task_id: uuid.UUID, db=Depends(get_db)):
    """Retrieve all Incident for a specific task."""
    return db_task_incident.get_all_task_dependency(db, task_id)


@router.delete('/delete/{task_incident_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(task_incident_id: uuid.UUID, db=Depends(get_db)):
    """Delete a task incident by its ID."""
    if not db_task_incident.delete(task_incident_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return {"detail": f"Incident with id:{task_incident_id} deleted successfully"}
