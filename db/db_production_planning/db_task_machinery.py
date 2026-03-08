from fastapi import HTTPException, status
from routers.schemas import TaskMachineryBase
from fastapi.responses import JSONResponse
import uuid
from db.supabase_client import supabase


def create_task_machinery(request: TaskMachineryBase, task_id: uuid.UUID, machinery_id: uuid.UUID, user=None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        task_machinery_data = {
            "task_id": str(task_id),
            "machinery_id": str(machinery_id)
        }

        result = (supabase.table("task_machinery").insert(task_machinery_data).execute())

        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create task machinery")

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all_task_machinery(task_id: uuid.UUID, offset: int = 0, limit: int = 20):
    count_response = (
        supabase.table("task_machinery")
        .select("*", count="exact")
        .eq("task_id", str(task_id))
        .limit(0)
        .execute()
    )
    total = count_response.count or 0

    response = (
        supabase.table("task_machinery")
        .select("*")
        .eq("task_id", str(task_id))
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or [], total


def delete(id: uuid.UUID):
    response = supabase.table("task_machinery").delete().eq("task_machinery_id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task machinery with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Task machinery with id:{id}"})
