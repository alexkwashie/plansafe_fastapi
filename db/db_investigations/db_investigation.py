import uuid
from datetime import datetime
from fastapi import HTTPException, status
from routers.schemas import InvestigationBase, InvestigationUpdate
from db.supabase_client import supabase


def create_investigation(incident_id: uuid.UUID, request: InvestigationBase, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        data = {
            "incident_id": str(incident_id),
            "assigned_to": str(request.assigned_to) if request.assigned_to else None,
            "investigation_type": request.investigation_type.value if request.investigation_type else None,
            "findings": request.findings,
            "root_cause": request.root_cause,
        }

        result = supabase.table("investigations").insert(data).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create investigation"
            )
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_investigations_for_incident(incident_id: uuid.UUID, offset: int = 0, limit: int = 20):
    count_response = (
        supabase.table("investigations")
        .select("*", count="exact")
        .eq("incident_id", str(incident_id))
        .limit(0)
        .execute()
    )
    total = count_response.count or 0

    response = (
        supabase.table("investigations")
        .select("*")
        .eq("incident_id", str(incident_id))
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or [], total


def get_by_id(investigation_id: uuid.UUID):
    response = supabase.table("investigations").select("*").eq("investigation_id", str(investigation_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Investigation not found")
    return response.data[0]


def update_investigation(investigation_id: uuid.UUID, request: InvestigationUpdate, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        update_data = {}
        if request.assigned_to is not None:
            update_data["assigned_to"] = str(request.assigned_to)
        if request.status is not None:
            update_data["status"] = request.status.value
            if request.status.value == "closed":
                update_data["closed_at"] = datetime.utcnow().isoformat()
        if request.investigation_type is not None:
            update_data["investigation_type"] = request.investigation_type.value
        if request.findings is not None:
            update_data["findings"] = request.findings
        if request.root_cause is not None:
            update_data["root_cause"] = request.root_cause

        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        update_data["updated_at"] = datetime.utcnow().isoformat()

        result = supabase.table("investigations").update(update_data).eq("investigation_id", str(investigation_id)).execute()

        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Investigation with id: {investigation_id} not found")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))
