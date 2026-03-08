import uuid
from datetime import datetime
from fastapi import HTTPException, status
from routers.schemas import InspectionBase, InspectionUpdate, InspectionResponseBase
from db.supabase_client import supabase


def create_inspection(request: InspectionBase, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        data = {
            "template_id": str(request.template_id),
            "inspector_id": str(request.inspector_id) if request.inspector_id else (user.get("user_id") if user else None),
            "scheduled_date": request.scheduled_date.isoformat() if request.scheduled_date else None,
            "notes": request.notes,
        }

        result = supabase.table("inspections").insert(data).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create inspection")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all_inspections(offset: int = 0, limit: int = 20, status_filter: str = None, date_from: str = None, date_to: str = None):
    query = supabase.table("inspections").select("*", count="exact")

    if status_filter:
        query = query.eq("status", status_filter)
    if date_from:
        query = query.gte("scheduled_date", date_from)
    if date_to:
        query = query.lte("scheduled_date", date_to)

    count_response = query.limit(0).execute()
    total = count_response.count or 0

    data_query = supabase.table("inspections").select("*")
    if status_filter:
        data_query = data_query.eq("status", status_filter)
    if date_from:
        data_query = data_query.gte("scheduled_date", date_from)
    if date_to:
        data_query = data_query.lte("scheduled_date", date_to)

    response = data_query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()
    return response.data or [], total


def get_by_id(inspection_id: uuid.UUID):
    response = supabase.table("inspections").select("*").eq("inspection_id", str(inspection_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspection not found")
    return response.data[0]


def get_with_responses(inspection_id: uuid.UUID):
    """Get inspection with all its responses."""
    inspection = get_by_id(inspection_id)
    responses = (
        supabase.table("inspection_responses")
        .select("*")
        .eq("inspection_id", str(inspection_id))
        .execute()
    )
    inspection["responses"] = responses.data or []
    return inspection


def update_inspection(inspection_id: uuid.UUID, request: InspectionUpdate, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        update_data = {}
        if request.status is not None:
            update_data["status"] = request.status.value
            if request.status.value == "completed":
                update_data["completed_at"] = datetime.utcnow().isoformat()
        if request.scheduled_date is not None:
            update_data["scheduled_date"] = request.scheduled_date.isoformat()
        if request.notes is not None:
            update_data["notes"] = request.notes

        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        result = supabase.table("inspections").update(update_data).eq("inspection_id", str(inspection_id)).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspection not found")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def submit_response(inspection_id: uuid.UUID, request: InspectionResponseBase):
    try:
        data = {
            "inspection_id": str(inspection_id),
            "template_item_id": str(request.template_item_id),
            "response": request.response.value,
            "notes": request.notes,
            "photo_url": request.photo_url,
        }

        result = supabase.table("inspection_responses").insert(data).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to submit response")

        # If response is "fail", create a follow-up task in the first active batch
        if request.response.value == "fail":
            _create_followup_task(inspection_id, request)

        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def _create_followup_task(inspection_id: uuid.UUID, response: InspectionResponseBase):
    """Create a follow-up task for a failed inspection item."""
    try:
        # Get the template item text
        item = supabase.table("checklist_template_items").select("item_text").eq("item_id", str(response.template_item_id)).execute()
        item_text = item.data[0]["item_text"] if item.data else "Unknown item"

        # Find an active batch to attach the task to
        batch = supabase.table("batch_table").select("batch_id").eq("batch_status", "in_progress").limit(1).execute()
        if not batch.data:
            print("[Inspection] No active batch found for follow-up task. Skipping.")
            return

        batch_id = batch.data[0]["batch_id"]

        task_data = {
            "batch_id": batch_id,
            "task_name": f"Follow-up: {item_text}",
            "task_description": f"Auto-generated from failed inspection item. Inspection ID: {inspection_id}. Notes: {response.notes or 'None'}",
            "status": "pending",
        }
        supabase.table("task_table").insert(task_data).execute()

    except Exception as error:
        print(f"[Inspection] Failed to create follow-up task: {error}")
