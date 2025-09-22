from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import verify_token
from routers.schemas import UserDisplay
from db import db_user
from typing import List
import uuid


router = APIRouter(
    prefix='/user',
    tags=['users']
)


@router.get('/all-users/', response_model=List[UserDisplay])
def all_users():
    return db_user.get_all_users()


@router.put('/{id}', response_model=UserDisplay)
def get_user_by_id(uid: uuid.UUID, request: UserDisplay):
    """get user by its ID."""
    return db_user.get_current_user(uid)

