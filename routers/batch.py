from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import verify_jwt
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
def create(request: BatchBase, db=Depends(get_db), user=Depends(verify_jwt)):
    return db_batch.create_batch(db, request)


@router.get('/all', response_model=List[BatchDisplay])
async def batchs(db=Depends(get_db), user=Depends(verify_jwt)):
    return db_batch.get_all(db)


@router.get('/delete/{id}')
def delete(id: int, db=Depends(get_db), user=Depends(verify_jwt)):
    return db_batch.delete(id, db)
