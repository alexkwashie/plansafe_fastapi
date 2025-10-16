from fastapi import HTTPException, status
from routers.schemas import TaskMachineryBase
from fastapi.responses import JSONResponse
from supabase import create_client
import os
import uuid

auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def create_task_machinery(request: TaskMachineryBase, user, task_id: uuid.UUID, machinery_id:uuid.UUID):
    try:
        # Create Supabase client with the user's token
        if user and "access_token" in user and "refresh_token" in user:
            auth_supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        # Prepare the data dictionary for insertion
        task_machinery_data = {
            "task_id": str(task_id),
            "machinery_id": str(machinery_id)
            }

        result = (auth_supabase.table("task_machinery").insert(task_machinery_data).execute())
        

        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create task machinery")

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))





def get_all_task_machinery(db, task_id: uuid.UUID):
    response = db.table("task_machinery").select("*").eq("task_id", task_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to get related task machinery")
    tasks_machinery = response.data

    
    return tasks_machinery



def delete(id: uuid.UUID, db):
    response = db.table("task_machinery").delete().eq("task_machinery_id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task Dependency with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Task incident with id:{id}"})
