from fastapi import HTTPException, status
from routers.schemas import TaskBase, TaskUpdateBase
from fastapi.responses import JSONResponse
from datetime import datetime, time
from supabase import create_client
import os
import uuid

auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def normalize_record(record: dict) -> dict:
    """
    Convert UUIDs and datetime objects to strings
    so they can be JSON serialized.
    """
    for k, v in record.items():
        if isinstance(v, (uuid.UUID, datetime)):
            record[k] = str(v)
    return record

def create_task(request: TaskBase, batch_id: uuid.UUID):
    print("Incoming request data:", request.dict())
    try:
        def to_time_str(value):
            if isinstance(value, time):
                return value.strftime("%H:%M:%S")
            if isinstance(value, str):
                return value
            return None

        # Prepare the data dictionary for insertion
        task_data = {
            "batch_id": str(batch_id),
            "task_seq": request.task_seq,
            "task_name": request.task_name,
            "task_description": request.task_description,
            "task_notes": request.task_notes,
            "estimated_duration": request.estimated_duration,
            "status": request.status or "pending",
            "output_product": request.output_product,
            "outputs_quantity": request.outputs_quantity,
            "start_time": to_time_str(request.start_time),
            "end_time": to_time_str(request.end_time),
            "created_by": str(request.created_by) if request.created_by else None,
            "created_at": (
                request.created_at.isoformat() if request.created_at else None
            )
        }

        result = auth_supabase.table("task_table").insert(task_data).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create task"
            )

        return normalize_record(result.data[0])

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))



def get_all_task(batch_id: uuid.UUID):
    try:
        response = auth_supabase.table("task_table").select("*").eq("batch_id", str(batch_id)).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch tasks")
        tasks = response.data
        # Convert UUIDs and datetimes to strings
        for rec in tasks:
            for k, v in rec.items():
                if isinstance(v, (uuid.UUID, datetime)):
                    rec[k] = str(v)
        return tasks
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def delete(task_id: uuid.UUID):
    response = auth_supabase.table("task_table").delete().eq("task_id", str(task_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Task with id:{task_id}"})


def update_task(task_id: uuid.UUID, request: TaskUpdateBase):
    try:
        def to_time_str(value):
            if isinstance(value, time):
                return value.strftime("%H:%M:%S")
            if isinstance(value, str):
                return value
            return None

        task_data = {
            "task_seq": request.task_seq,
            "task_name": request.task_name,
            "task_description": request.task_description,
            "task_notes": request.task_notes,
            "estimated_duration": request.estimated_duration,
            "status": request.status or "pending",
            "output_product": request.output_product,
            "outputs_quantity": request.outputs_quantity,
            "start_time": to_time_str(request.start_time),
            "end_time": to_time_str(request.end_time),
            "updated_by": str(request.updated_by) if request.updated_by else None,
            "updated_at": (request.updated_at.isoformat() if request.updated_at else None)
        }
        
        result = auth_supabase.table("task_table").update(task_data).eq("task_id", str(task_id)).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {task_id} not found")
        record = result.data[0]
        
        for k, v in record.items():
            if isinstance(v, (uuid.UUID, datetime)):
                record[k] = str(v)
        return record
    
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))
