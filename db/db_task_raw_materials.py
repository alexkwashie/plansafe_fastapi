from fastapi import HTTPException, status
from routers.schemas import TaskRawMaterialBase
from fastapi.responses import JSONResponse
from supabase import create_client
import os
import uuid

auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def create_task_raw_material(db, request: TaskRawMaterialBase, task_id: uuid.UUID, raw_material_id: uuid.UUID,user: dict = None):
    try:
        # Create Supabase client with the user's token
        if user and "access_token" in user and "refresh_token" in user:
            auth_supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )
            
        raw_material_item = db.table("raw_materials").select("*").eq("raw_material_id", raw_material_id).execute()
        
        # Prepare the data dictionary for insertion
        task_raw_material_data = {
            "task_id": str(task_id),
            "raw_material_id": str(raw_material_id),
            "material_name": raw_material_item.material_name,
            "assigned_quantity": request.assigned_quantity
            }

        result = (auth_supabase.table("task_raw_material").insert(task_raw_material_data).execute())
        

        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create task raw material")

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))





def get_all_task_raw_material(db, task_id: uuid.UUID):
    response = db.table("task_raw_material").select("*").eq("task_id", task_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to get related task raw material")
    task_raw_material = response.data

    
    return task_raw_material



def delete(id: uuid.UUID, db):
    response = db.table("task_raw_material").delete().eq("task_machinery_id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task Raw material with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Task raw material with id:{id}"})
