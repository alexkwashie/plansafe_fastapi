from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import MachineryDisplay, MachineryBase
from db.database import get_db
from db import db_machinery
from typing import List
from routers.schemas import UserAuth


router = APIRouter(
    prefix='/machinery',
    tags=['machinery']
)


@router.post('/create-machinery', response_model=MachineryDisplay)
def create(request: MachineryBase, db=Depends(get_db), current_user: UserAuth = Depends(verify_token)):
    return db_machinery.create_machinery(db, request, current_user)


@router.get('/all-machinery', response_model=List[MachineryDisplay])
def all_machinery(db=Depends(get_db)):
    return db_machinery.get_all_machinery(db)


@router.get('/delete/{id}')
def delete(id: int, db=Depends(get_db)):
    return db_machinery.delete(id, db)


