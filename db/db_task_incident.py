from fastapi import HTTPException, status
from routers.schemas import TaskIncidentBase
from fastapi.responses import JSONResponse
from supabase import create_client
import os
import uuid

auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def create_task_incient(db, request: TaskIncidentBase, user, task_id: uuid.UUID):
    try:
        # Create Supabase client with the user's token
        auth_supabase.auth.set_session(user["access_token"], user["refresh_token"])

        # Prepare the data dictionary for insertion
        task_incident_data = {
            "task_id": task_id,
            "task_incident_id": request.task_incident_id
            }

        
        result = (auth_supabase.table("task_incident").insert(task_incident_data).execute())
        

        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to task incident task")

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))





def get_all_task_incident(db, task_id: uuid.UUID):
    response = db.table("task_incidents").select("*").eq("task_id", task_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to related task incident")
    tasks_assignee = response.data

    
    return tasks_assignee



def delete(task_incident_id: uuid.UUID, db):
    response = db.table("task_incidents").delete().eq("task_incident", task_incident_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task Dependency with id: {task_incident_id} not found")
    return JSONResponse(content={"message": f"Deleted: Task incident with id:{task_incident_id}"})
