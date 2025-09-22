from fastapi import HTTPException, status
from routers.schemas import TaskAssigneeBase
from fastapi.responses import JSONResponse
from supabase import create_client
import os
import uuid

auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def create_task_assignees(task_id: uuid.UUID, user_id: uuid.UUID, user: dict = None):
    try:
        # Create Supabase client with the user's token
        if user and "access_token" in user and "refresh_token" in user:
            auth_supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        # Prepare the data dictionary for insertion
        task_assignee_data = {
            "task_id": str(task_id),
            "user_id": str(user_id)
    
        }

        result = (
            auth_supabase.table("task_assignees").insert(task_assignee_data).execute()
        )
        

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create task"
            )

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))





def get_all_task_assignee(task_id: uuid.UUID):
    response = auth_supabase.table("task_assignees").select("*").eq("task_id", task_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch tasks")
    tasks_assignee = response.data
    
    print(tasks_assignee)
    
    return tasks_assignee
    



def delete(assignees_id: uuid.UUID, db):
    response = db.table("tasks").delete().eq("assignees_id", assignees_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Task assignee with id:{assignees_id}"})
