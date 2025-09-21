import uuid
from fastapi import HTTPException, status, Depends
from routers.schemas import BatchBase, BatchBaseUpdate
from fastapi.responses import JSONResponse
from supabase import create_client
import os
from datetime import time, datetime


auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def create_batch(request: BatchBase, user: dict = None):
    try:
        # Create Supabase client with the user's token
        #auth_supabase.auth.set_session(user["access_token"], user["refresh_token"])
        
        # If a user and tokens are provided, set their session
        if user and "access_token" in user and "refresh_token" in user:
            auth_supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        
        def to_time_str(value):
            if isinstance(value, time):
                return value.strftime("%H:%M:%S")
            if isinstance(value, str):
                return value  # assume already valid like "08:00" or "08:00:00"
            return None
        
        result = (
            auth_supabase.table("batch_table")
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

        # Convert estimated_duration and process_duration to strings if they exist
        batch_data = result.data[0]
        if "estimated_duration" in batch_data and batch_data["estimated_duration"] is not None:
            batch_data["estimated_duration"] = str(batch_data["estimated_duration"])
        if "process_duration" in batch_data and batch_data["process_duration"] is not None:
            batch_data["process_duration"] = str(batch_data["process_duration"])

        return batch_data

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))




def get_all():
    response = auth_supabase.table("batch_table").select("*").execute()

    # Safely handle empty or invalid response
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No batch data returned"
        )

    batches = response.data

    return batches



def delete(id: uuid.UUID):
    response = auth_supabase.table("batch_table").delete().eq("batch_id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Batch with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Batch with id:{id}"})



def update_batch(id: uuid.UUID, request: BatchBaseUpdate, user: dict = None):
    """Update a batch by its ID."""
    try:
        # Create Supabase client with the user's token if available
        if user and "access_token" in user and "refresh_token" in user:
            auth_supabase.auth.set_session(user["access_token"], user["refresh_token"])

        def to_time_str(value):
            if isinstance(value, time):
                return value.strftime("%H:%M:%S")
            if isinstance(value, str):
                return value  # assume already valid like "08:00" or "08:00:00"
            return None
        
        # Prepare the data dictionary for updating
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
            "updated_by": str(request.updated_by),
            "updated_at": request.updated_at.isoformat() if request.updated_at else None,
        }

        result = (
            auth_supabase.table("batch_table").update(updated_batch_data).eq("batch_id", id).execute()
        )
        
        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} not found")
        record = result.data[0]
        
        for k, v in record.items():
            if isinstance(v, (uuid.UUID, datetime)):
                record[k] = str(v)
        
        return record

    except Exception as error:
        print(f"======= {error}->->->")
        raise HTTPException(status_code=500, detail=str(error))
