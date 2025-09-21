from fastapi import HTTPException, status
from routers.schemas import MachineryBase
from fastapi.responses import JSONResponse
from supabase import create_client
import os
import uuid

auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def create_machinery(db, request: MachineryBase, user):
    try:
        # Create Supabase client with the user's token
        auth_supabase.auth.set_session(user["access_token"], user["refresh_token"])

        # Prepare the data dictionary for insertion
        machinery_data = {
           "machine_name": request.machine_name,
            "machine_type": request.machine_type,
            "machine_manufacture": request.machine_manufacture,
            "location": request.location,
            "status": request.status or "pending",
            "capacity":request.capacity,
            "power_rating": request.power_rating,
            "created_by": request.created_by,
            "updated_by": request.user_id
    
        }

        result = (
            auth_supabase.table("machinery").insert(machinery_data).execute()
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





def get_all_machinery(db):
    response = db.table("machinery").select("*").execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch machinery data")
    machinery_data = response.data

    
    return machinery_data



def delete(machiner_id: uuid.UUID, db):
    response = db.table("machinery").delete().eq("machinery_id", machiner_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machinery with id: {machiner_id} not found")
    return JSONResponse(content={"message": f"Deleted: Machinery with id:{machiner_id}"})
