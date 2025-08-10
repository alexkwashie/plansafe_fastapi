from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import TaskBase, TaskDisplay
from db.database import get_db
from db import db_task
from typing import List
from routers.schemas import UserAuth


router = APIRouter(
    prefix='/task',
    tags=['task']
)


@router.post('/create-task', response_model=TaskDisplay)
def create(request: TaskBase, db=Depends(get_db), current_user: UserAuth = Depends(verify_token)):
    return db_task.create_task(db, request, current_user)


@router.get('/all/{batch_id}', response_model=List[TaskDisplay])
def all_task(batch_id: int, db=Depends(get_db)):
    return db_task.get_all_task(db, batch_id)


@router.get('/delete/{id}')
def delete(id: int, db=Depends(get_db)):
    return db_task.delete(id, db)
