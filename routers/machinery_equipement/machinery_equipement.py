import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import MachineryDisplay,MachineryBase, MachineryBaseUpdate
from db.db_machinery_equipement import db_machinery_equipement
from typing import List


router = APIRouter(
    prefix='/machinery',
    tags=['machinery']
)


@router.post('/create-machinery', response_model=MachineryDisplay)
def create(request: MachineryBase, user=Depends(verify_token)):
    return db_machinery_equipement.create_machinery(request, user)

@router.get('/all', response_model=List[MachineryDisplay])
def all_machinery():
    return db_machinery_equipement.get_all_machinery()

@router.put('/update/{id}', response_model=MachineryDisplay)
def update(id: uuid.UUID, request: MachineryBaseUpdate):
    """Update a machinery by its ID."""
    return db_machinery_equipement.update_machinery(id, request)

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: uuid.UUID):
    """Delete a task machinery by its ID."""
    if not db_machinery_equipement.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Related Machinery not found")
    return {"detail": f"Machinery with id:{id} deleted successfully"}

