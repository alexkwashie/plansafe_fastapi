from fastapi import HTTPException, status
from routers.schemas import TaskDependencyBase
from fastapi.responses import JSONResponse
from supabase import create_client
import os
import uuid

auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def create_task_dependency(db, request: TaskDependencyBase, user, task_id_1: uuid.UUID, task_id_2: uuid.UUID):
    try:
        # Create Supabase client with the user's token
        auth_supabase.auth.set_session(user["access_token"], user["refresh_token"])

        # Prepare the data dictionary for insertion
        task_dependency_data = {
            "seq_no": request.seq_no,
            "task_id_1": task_id_1,
            "task_id_2": task_id_2
            }

        result = (auth_supabase.table("task_dependency").insert(task_dependency_data).execute())
        

        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to task dependency task")

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))





def get_all_task_dependency(db, task_id_1: uuid.UUID):
    response = db.table("task_dependency").select("*").eq("task_id", task_id_1).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to related task dependency")
    tasks_assignee = response.data

    
    return tasks_assignee



def delete(dependency_id: uuid.UUID, db):
    response = db.table("task_dependency").delete().eq("dependency_id", dependency_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task Dependency with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Task dependency with id:{dependency_id}"})
