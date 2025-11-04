import uuid
from fastapi import HTTPException, status, Depends
from routers.schemas import MachineryBase, MachineryBaseUpdate
from fastapi.responses import JSONResponse
from supabase import create_client
import os


auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def create_machinery(request: MachineryBase, user: dict = None):
    try:
        # Create Supabase client with the user's token
        #auth_supabase.auth.set_session(user["access_token"], user["refresh_token"])
        
        # If a user and tokens are provided, set their session
        if user and "access_token" in user and "refresh_token" in user:
            auth_supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        
        result = (
            auth_supabase.table("machinery")
            .insert({
                "machine_name": request.machine_name,
                "machine_type": request.machine_type,
                "machine_manufacture": request.machine_manufacture,
                "location": request.location,
                "status": request.status,
                "capacity": request.capacity,
                "power_rating": request.power_rating,
                "created_at": request.created_at.isoformat() if request.created_at else None,
                "created_by": str(request.created_by)
            })
            .execute()
        )


        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add machinery"
            )

        machinery_data = result.data[0]
        
        return machinery_data

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))




def get_all_machinery():
    response = auth_supabase.table("machinery").select("*").execute()

    # Safely handle empty or invalid response
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No batch data returned"
        )

    machinery = response.data

    return machinery



def delete(id: uuid.UUID):
    response = auth_supabase.table("machinery").delete().eq("machinery_id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Batch with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Machinery with id:{id}"})



def update_machinery(id: uuid.UUID, request: MachineryBaseUpdate, user: dict = None):
    """Update a machinery by its ID."""
    try:
        # Create Supabase client with the user's token if available
        if user and "access_token" in user and "refresh_token" in user:
            auth_supabase.auth.set_session(user["access_token"], user["refresh_token"])

        
        # Prepare the data dictionary for updating
        updated_machinery_data = {
                "machine_name": request.machine_name,
                "machine_type": request.machine_type,
                "machine_manufacture": request.machine_manufacture,
                "location": request.location,
                "status": request.status,
                "capacity": request.capacity,
                "power_rating": request.power_rating,
                "updated_by": str(request.updated_by),
                "updated_at": request.updated_at.isoformat() if request.updated_at else None,
        }

        result = (
            auth_supabase.table("machinery").update(updated_machinery_data).eq("machinery_id", id).execute()
        )
        
        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} not found")
        record = result.data[0]
        
        return record

    except Exception as error:
        print(f"======= {error}->->->")
        raise HTTPException(status_code=500, detail=str(error))
