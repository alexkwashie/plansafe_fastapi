from fastapi import HTTPException, status
from routers.schemas import TaskBase, TaskUpdateBase
from fastapi.responses import JSONResponse
from datetime import datetime, time
import uuid
from db.supabase_client import supabase


def normalize_record(record: dict) -> dict:
    for k, v in record.items():
        if isinstance(v, (uuid.UUID, datetime)):
            record[k] = str(v)
    return record


def create_task(request: TaskBase, batch_id: uuid.UUID):
    try:
        def to_time_str(value):
            if isinstance(value, time):
                return value.strftime("%H:%M:%S")
            if isinstance(value, str):
                return value
            return None

        task_data = {
            "batch_id": str(batch_id),
            "task_name": request.task_name,
            "task_description": request.task_description,
            "task_notes": request.task_notes,
            "estimated_duration": request.estimated_duration,
            "status": request.status.value if request.status else "pending",
            "output_product": request.output_product,
            "outputs_quantity": request.outputs_quantity,
            "start_time": to_time_str(request.start_time),
            "end_time": to_time_str(request.end_time),
            "sequence_order": request.sequence_order,
            "depends_on_task_id": str(request.depends_on_task_id) if request.depends_on_task_id else None,
            "sop_document_url": request.sop_document_url,
            "created_by": str(request.created_by) if request.created_by else None,
            "created_at": (
                request.created_at.isoformat() if request.created_at else None
            )
        }

        result = supabase.table("task_table").insert(task_data).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create task"
            )

        return normalize_record(result.data[0])

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all_task(batch_id: uuid.UUID, offset: int = 0, limit: int = 20):
    try:
        count_response = (
            supabase.table("task_table")
            .select("*", count="exact")
            .eq("batch_id", str(batch_id))
            .limit(0)
            .execute()
        )
        total = count_response.count or 0

        response = (
            supabase.table("task_table")
            .select("*")
            .eq("batch_id", str(batch_id))
            .range(offset, offset + limit - 1)
            .execute()
        )

        tasks = response.data or []
        for rec in tasks:
            for k, v in rec.items():
                if isinstance(v, (uuid.UUID, datetime)):
                    rec[k] = str(v)
        return tasks, total

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_by_id(task_id: uuid.UUID):
    response = supabase.table("task_table").select("*").eq("task_id", str(task_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return normalize_record(response.data[0])


def delete(task_id: uuid.UUID):
    response = supabase.table("task_table").delete().eq("task_id", str(task_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {task_id} not found")
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
            "task_name": request.task_name,
            "task_description": request.task_description,
            "task_notes": request.task_notes,
            "estimated_duration": request.estimated_duration,
            "status": request.status.value if request.status else "pending",
            "output_product": request.output_product,
            "outputs_quantity": request.outputs_quantity,
            "start_time": to_time_str(request.start_time),
            "end_time": to_time_str(request.end_time),
            "sequence_order": request.sequence_order,
            "depends_on_task_id": str(request.depends_on_task_id) if request.depends_on_task_id else None,
            "sop_document_url": request.sop_document_url,
            "updated_by": str(request.updated_by) if request.updated_by else None,
            "updated_at": (request.updated_at.isoformat() if request.updated_at else None)
        }

        result = supabase.table("task_table").update(task_data).eq("task_id", str(task_id)).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {task_id} not found")
        return normalize_record(result.data[0])

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))
