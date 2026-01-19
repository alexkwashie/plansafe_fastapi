from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import RawMaterialBase, RawMaterialDisplay, RawMaterialUpdate
from db.database import get_db
from db.db_raw_materials import db_raw_material
from typing import List
from routers.schemas import UserAuth
import uuid


router = APIRouter(
    prefix='/raw-material',
    tags=['raw-material']
)


@router.post('/create-raw-material', response_model=RawMaterialDisplay)
def create(request: RawMaterialBase, user=Depends(verify_token)):
    return db_raw_material.create_raw_material(request, user)


@router.get('/all-raw-material', response_model=List[RawMaterialDisplay])
def all_machinery():
    return db_raw_material.get_all_raw_material()


@router.put('/update/{id}', response_model=RawMaterialDisplay)
def update(id: uuid.UUID, request: RawMaterialUpdate):
    """Update a rawmaterial by its ID."""
    return db_raw_material.update_raw_material(id, request)


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: uuid.UUID):
    """Delete a task raw materials by its ID."""
    if not db_raw_material.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Related Raw material not found")
    return {"detail": f"Raw material with id:{id} deleted successfully"}


