from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import uuid
from db.supabase_client import supabase


def create_task_assignees(task_id: uuid.UUID, user_id: uuid.UUID, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        task_assignee_data = {
            "task_id": str(task_id),
            "user_id": str(user_id)
        }

        result = (
            supabase.table("task_assignees").insert(task_assignee_data).execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create task assignee"
            )

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all_task_assignee(task_id: uuid.UUID, offset: int = 0, limit: int = 20):
    count_response = (
        supabase.table("task_assignees")
        .select("*", count="exact")
        .eq("task_id", str(task_id))
        .limit(0)
        .execute()
    )
    total = count_response.count or 0

    response = (
        supabase.table("task_assignees")
        .select("*")
        .eq("task_id", str(task_id))
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or [], total


def delete(task_assignees_id: uuid.UUID):
    response = supabase.table("task_assignees").delete().eq("assignees_id", task_assignees_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task assignee with id: {task_assignees_id} not found")
    return JSONResponse(content={"message": f"Deleted: Task assignee with id:{task_assignees_id}"})
