import uuid
from fastapi import HTTPException, status
from routers.schemas import NoteBase, NoteUpdate
from db.supabase_client import supabase


VALID_ENTITY_TYPES = {"batch", "task", "equipment", "incident"}


def create_note(entity_type: str, entity_id: uuid.UUID, request: NoteBase, user: dict = None):
    if entity_type not in VALID_ENTITY_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid entity_type: {entity_type}. Must be one of {VALID_ENTITY_TYPES}"
        )

    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        note_data = {
            "entity_type": entity_type,
            "entity_id": str(entity_id),
            "note_type": request.note_type.value if request.note_type else "general",
            "content": request.content,
            "photo_url": request.photo_url,
            "created_by": user.get("user_id") if user else None,
        }

        result = supabase.table("notes").insert(note_data).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create note"
            )

        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_notes_for_entity(entity_type: str, entity_id: uuid.UUID, offset: int = 0, limit: int = 20):
    if entity_type not in VALID_ENTITY_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid entity_type: {entity_type}. Must be one of {VALID_ENTITY_TYPES}"
        )

    count_response = (
        supabase.table("notes")
        .select("*", count="exact")
        .eq("entity_type", entity_type)
        .eq("entity_id", str(entity_id))
        .limit(0)
        .execute()
    )
    total = count_response.count or 0

    response = (
        supabase.table("notes")
        .select("*")
        .eq("entity_type", entity_type)
        .eq("entity_id", str(entity_id))
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or [], total


def get_by_id(note_id: uuid.UUID):
    response = supabase.table("notes").select("*").eq("note_id", str(note_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return response.data[0]


def update_note(note_id: uuid.UUID, request: NoteUpdate, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        update_data = {}
        if request.note_type is not None:
            update_data["note_type"] = request.note_type.value
        if request.content is not None:
            update_data["content"] = request.content
        if request.photo_url is not None:
            update_data["photo_url"] = request.photo_url

        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        result = supabase.table("notes").update(update_data).eq("note_id", str(note_id)).execute()

        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id: {note_id} not found")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def delete_note(note_id: uuid.UUID):
    response = supabase.table("notes").delete().eq("note_id", str(note_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id: {note_id} not found")
    return True
