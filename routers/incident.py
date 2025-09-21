from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import IncidentBase, IncidentDisplay
from db.database import get_db
from db import db_incident
from typing import List
from routers.schemas import UserAuth
import uuid


router = APIRouter(
    prefix='/incidents',
    tags=['incidents']
)


@router.post('/create/{task_id}', response_model=IncidentBase)
def create(request: IncidentBase, task_id: uuid.UUID, db=Depends(get_db), current_user: UserAuth = Depends(verify_token)):
    return db_incident.create_task_raw_material(db, request, task_id, current_user)


@router.get('/all/{task_id}', response_model=List[IncidentDisplay])
def all_task_raw_materials(task_id: uuid.UUID, db=Depends(get_db)):
    return db_incident.get_all_task_raw_material(db, task_id)


@router.delete('/delete/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(task_incident_id: uuid.UUID, db=Depends(get_db)):
    """Delete a task raw materials by its ID."""
    if not db_incident.delete(task_incident_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task raw material not found")
    return {"detail": f"Task Raw Materials {task_raw_material_id} deleted successfully"}


