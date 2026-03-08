import uuid
from datetime import datetime
from fastapi import HTTPException, status
from routers.schemas import CAPABase, CAPAUpdate
from db.supabase_client import supabase


def create_capa(investigation_id: uuid.UUID, request: CAPABase, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        data = {
            "investigation_id": str(investigation_id),
            "action_type": request.action_type.value,
            "description": request.description,
            "assigned_to": str(request.assigned_to) if request.assigned_to else None,
            "due_date": request.due_date.isoformat() if request.due_date else None,
        }

        result = supabase.table("capa_actions").insert(data).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create CAPA action"
            )
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_capas_for_investigation(investigation_id: uuid.UUID, offset: int = 0, limit: int = 20):
    count_response = (
        supabase.table("capa_actions")
        .select("*", count="exact")
        .eq("investigation_id", str(investigation_id))
        .limit(0)
        .execute()
    )
    total = count_response.count or 0

    response = (
        supabase.table("capa_actions")
        .select("*")
        .eq("investigation_id", str(investigation_id))
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or [], total


def get_by_id(capa_id: uuid.UUID):
    response = supabase.table("capa_actions").select("*").eq("capa_id", str(capa_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CAPA action not found")
    return response.data[0]


def update_capa(capa_id: uuid.UUID, request: CAPAUpdate, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        update_data = {}
        if request.action_type is not None:
            update_data["action_type"] = request.action_type.value
        if request.description is not None:
            update_data["description"] = request.description
        if request.assigned_to is not None:
            update_data["assigned_to"] = str(request.assigned_to)
        if request.due_date is not None:
            update_data["due_date"] = request.due_date.isoformat()
        if request.status is not None:
            update_data["status"] = request.status.value
            if request.status.value == "completed":
                update_data["completed_at"] = datetime.utcnow().isoformat()

        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        result = supabase.table("capa_actions").update(update_data).eq("capa_id", str(capa_id)).execute()

        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CAPA action with id: {capa_id} not found")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def delete_capa(capa_id: uuid.UUID):
    response = supabase.table("capa_actions").delete().eq("capa_id", str(capa_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CAPA action with id: {capa_id} not found")
    return True
