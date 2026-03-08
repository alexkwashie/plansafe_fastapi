import uuid
from fastapi import HTTPException, status
from routers.schemas import BatchBase, BatchBaseUpdate
from fastapi.responses import JSONResponse
from datetime import time, datetime
from db.supabase_client import supabase


def create_batch(request: BatchBase, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        def to_time_str(value):
            if isinstance(value, time):
                return value.strftime("%H:%M:%S")
            if isinstance(value, str):
                return value
            return None

        result = (
            supabase.table("batch_table")
            .insert({
                "batch_title": request.batch_title,
                "color": request.color,
                "start_date": request.start_date.isoformat() if hasattr(request.start_date, "isoformat") else request.start_date,
                "end_date": request.end_date.isoformat() if hasattr(request.end_date, "isoformat") else request.end_date,
                "batch_description": request.batch_description,
                "batch_status": str(request.batch_status),
                "start_time": to_time_str(request.start_time),
                "end_time": to_time_str(request.end_time),
                "location": request.location,
                "estimated_duration": request.estimated_duration,
                "process_duration": request.process_duration,
                "priority": request.priority.value if request.priority else "medium",
                "production_line": request.production_line,
                "created_at": request.created_at.isoformat() if request.created_at else None,
                "created_by": str(request.created_by),
            })
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create batch"
            )

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all(offset: int = 0, limit: int = 20):
    count_response = supabase.table("batch_table").select("*", count="exact").limit(0).execute()
    total = count_response.count or 0

    response = supabase.table("batch_table").select("*").range(offset, offset + limit - 1).execute()
    return response.data or [], total


def get_by_id(batch_id: uuid.UUID):
    response = supabase.table("batch_table").select("*").eq("batch_id", str(batch_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
    return response.data[0]


def delete(id: uuid.UUID):
    response = supabase.table("batch_table").delete().eq("batch_id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Batch with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Batch with id:{id}"})


def update_batch(id: uuid.UUID, request: BatchBaseUpdate, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        def to_time_str(value):
            if isinstance(value, time):
                return value.strftime("%H:%M:%S")
            if isinstance(value, str):
                return value
            return None

        updated_batch_data = {
            "batch_title": request.batch_title,
            "color": request.color,
            "start_date": request.start_date.isoformat() if hasattr(request.start_date, "isoformat") else request.start_date,
            "end_date": request.end_date.isoformat() if hasattr(request.end_date, "isoformat") else request.end_date,
            "batch_description": request.batch_description,
            "batch_status": str(request.batch_status),
            "start_time": to_time_str(request.start_time),
            "end_time": to_time_str(request.end_time),
            "location": request.location,
            "estimated_duration": request.estimated_duration,
            "process_duration": request.process_duration,
            "priority": request.priority.value if request.priority else None,
            "production_line": request.production_line,
            "updated_by": str(request.updated_by),
            "updated_at": request.updated_at.isoformat() if request.updated_at else None,
        }

        result = (
            supabase.table("batch_table").update(updated_batch_data).eq("batch_id", id).execute()
        )

        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Batch with id: {id} not found")
        return result.data[0]

    except Exception as error:
        print(f"======= {error}->->->")
        raise HTTPException(status_code=500, detail=str(error))
