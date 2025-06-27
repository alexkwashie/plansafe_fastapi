from auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from routers.schemas import BatchBase, BatchDisplay
from db.database import get_db
from db import db_batch
from typing import List
from routers.schemas import UserAuth


router = APIRouter(
  prefix='/batch',
  tags=['batch']
)


@router.post('/create-batch', response_model=BatchDisplay)
def create(request: BatchBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  return db_batch.create_batch(db, request)

@router.get('/all', response_model=List[BatchDisplay])
def batchs(db: Session = Depends(get_db)):
  return db_batch.get_all(db)


@router.get('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  return db_batch.delete(db, id, current_user.id)
