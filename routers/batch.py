import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import BatchBase, BatchDisplay, BatchBaseUpdate
from db.database import get_db
from db import db_batch
from typing import List


router = APIRouter(
    prefix='/batch',
    tags=['batch']
)


#Batch end points
#@router.post('/create-batch', response_model=BatchDisplay)
#def create(request: BatchBase, db=Depends(get_db)):
#    return db_batch.create_batch(db, request)

@router.post('/create-batch', response_model=BatchDisplay)
def create(request: BatchBase, user=Depends(verify_token)):
    return db_batch.create_batch(request, user)

@router.get('/all', response_model=List[BatchDisplay])
def batchs():
    return db_batch.get_all()

@router.put('/update/{id}', response_model=BatchDisplay)
def update(id: uuid.UUID, request: BatchBaseUpdate):
    """Update a task by its ID."""
    return db_batch.update_batch(id, request)

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: uuid.UUID):
    """Delete a task raw materials by its ID."""
    if not db_batch.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Related Task not found")
    return {"detail": f"Batch with id:{id} deleted successfully"}