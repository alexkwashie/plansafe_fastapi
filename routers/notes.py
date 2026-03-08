from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import NoteBase, NoteUpdate, NoteDisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_notes import db_note
import uuid


router = APIRouter(
    prefix='/api/v1',
    tags=['notes']
)


@router.post('/{entity_type}/{entity_id}/notes', response_model=NoteDisplay)
async def create(entity_type: str, entity_id: uuid.UUID, request: NoteBase, user=Depends(get_current_user)):
    return db_note.create_note(entity_type, entity_id, request, user)


@router.get('/{entity_type}/{entity_id}/notes')
async def list_notes_for_entity(entity_type: str, entity_id: uuid.UUID, pagination: PaginationParams = Depends()):
    data, total = db_note.get_notes_for_entity(entity_type, entity_id, offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/notes/{note_id}', response_model=NoteDisplay)
async def get_note(note_id: uuid.UUID):
    return db_note.get_by_id(note_id)


@router.put('/notes/{note_id}', response_model=NoteDisplay)
async def update(note_id: uuid.UUID, request: NoteUpdate, user=Depends(get_current_user)):
    return db_note.update_note(note_id, request, user)


@router.delete('/notes/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(note_id: uuid.UUID, user=Depends(get_current_user)):
    if not db_note.delete_note(note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
