from auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from routers.schemas import BatchBase, BatchDisplay, TaskBase, TaskDisplay
from db.database import get_db
from db import db_task
from typing import List
from routers.schemas import UserAuth


router = APIRouter(
  prefix='/task',
  tags=['task']
)


@router.post('/create-task', response_model=TaskDisplay)
def create(request: TaskBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  return db_task.create_task(db, request,current_user)

@router.get('/all/{batch_id}', response_model=List[TaskDisplay])
def all_task(batch_id: int, db: Session = Depends(get_db)):
  return db_task.get_all_task(db, batch_id)


@router.get('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  return db_task.delete(db, id)
