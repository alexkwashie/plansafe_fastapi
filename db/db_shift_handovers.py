import uuid
from datetime import datetime
from fastapi import HTTPException, status
from routers.schemas import ShiftHandoverBase
from db.supabase_client import supabase


def create_handover(request: ShiftHandoverBase, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        data = {
            "outgoing_user_id": user.get("user_id") if user else None,
            "incoming_user_id": str(request.incoming_user_id) if request.incoming_user_id else None,
            "shift_date": request.shift_date.isoformat(),
            "batch_status_summary": request.batch_status_summary,
            "outstanding_issues": request.outstanding_issues,
            "tasks_completed": request.tasks_completed,
            "tasks_remaining": request.tasks_remaining,
            "equipment_notes": request.equipment_notes,
            "incidents_occurred": request.incidents_occurred,
        }

        result = supabase.table("shift_handovers").insert(data).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create handover")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all_handovers(offset: int = 0, limit: int = 20, date_filter: str = None, user_filter: str = None):
    query = supabase.table("shift_handovers").select("*", count="exact")

    if date_filter:
        query = query.eq("shift_date", date_filter)
    if user_filter:
        query = query.or_(f"outgoing_user_id.eq.{user_filter},incoming_user_id.eq.{user_filter}")

    count_response = query.limit(0).execute()
    total = count_response.count or 0

    data_query = supabase.table("shift_handovers").select("*")
    if date_filter:
        data_query = data_query.eq("shift_date", date_filter)
    if user_filter:
        data_query = data_query.or_(f"outgoing_user_id.eq.{user_filter},incoming_user_id.eq.{user_filter}")

    response = data_query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()
    return response.data or [], total


def get_by_id(handover_id: uuid.UUID):
    response = supabase.table("shift_handovers").select("*").eq("handover_id", str(handover_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Handover not found")
    return response.data[0]


def acknowledge_handover(handover_id: uuid.UUID, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        update_data = {
            "acknowledged": True,
            "acknowledged_at": datetime.utcnow().isoformat(),
        }

        result = supabase.table("shift_handovers").update(update_data).eq("handover_id", str(handover_id)).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Handover not found")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))
