from fastapi import HTTPException, status
from routers.schemas import IncidentBase
from fastapi.responses import JSONResponse
from supabase import create_client
import os
import uuid

auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def create_machinery(db, request: IncidentBase, user, task_id: uuid.UUID):
    try:
        # Create Supabase client with the user's token
        auth_supabase.auth.set_session(user["access_token"], user["refresh_token"])

        # Prepare the data dictionary for insertion
        incident_data = {
            "task_incident_id": task_id, 
            "incident_name": request.incident_name,
            "incident_type": request.incident_type, 
            "incident_video_id": request.incident_video.id,
            "incident_voice_id": request.incident_voice_id,
            "incident_photo_id": request.incident_photo_id,
            "incident_time": request.incident_time,
            "incident_notes": request.incident_notes,
            "incident_severity": request.incident_severity,
            "incident_created_by": request.user_id
    
        }

        result = (
            auth_supabase.table("incidents").insert(incident_data).execute()
        )
        

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create machinery"
            )

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))





def get_all_incident(db, task_id: uuid.UUID):
    response = db.table("incidents").select("*").eq("task_incident_id", task_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch incident data")
    incident_data = response.data
    
    return incident_data


def delete(incident_id: uuid.UUID, db):
    response = db.table("incidents").delete().eq("machinery_id",incident_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machinery with id: {incident_id} not found")
    return JSONResponse(content={"message": f"Deleted: incident with id:{incident_id}"})
