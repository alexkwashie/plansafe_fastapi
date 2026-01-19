import uuid
from fastapi import HTTPException, status, Depends
from routers.schemas import RawMaterialDisplay, RawMaterialBase, RawMaterialUpdate
from fastapi.responses import JSONResponse
from supabase import create_client
import os


auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def create_raw_material(request: RawMaterialBase, user: dict = None):
    try:
        # Create Supabase client with the user's token
        #auth_supabase.auth.set_session(user["access_token"], user["refresh_token"])
        
        # If a user and tokens are provided, set their session
        if user and "access_token" in user and "refresh_token" in user:
            auth_supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        
        result = (
    auth_supabase.table("raw_materials").insert({
        "raw_material_id": str(uuid.uuid4()),
        "raw_material_name": request.raw_material_name,
        "raw_material_code": request.raw_material_code,
        "quantity": request.quantity,
        "reorder_level": request.reorder_level,
        "unit_cost": request.unit_cost,
        "category": request.category,
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

        raw_material_data = result.data[0]
        
        return raw_material_data

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))




def get_all_raw_material():
    response = auth_supabase.table("raw_materials").select("*").execute()

    # Safely handle empty or invalid response
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No raw material data returned"
        )

    raw_material = response.data

    return raw_material



def delete(id: uuid.UUID):
    response = auth_supabase.table("raw_materials").delete().eq("raw_material_id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Raw material with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Machinery with id:{id}"})



def update_raw_material(id: uuid.UUID, request: RawMaterialUpdate, user: dict = None):
    """Update a raw material by its ID."""
    try:
        # Create Supabase client with the user's token if available
        if user and "access_token" in user and "refresh_token" in user:
            auth_supabase.auth.set_session(user["access_token"], user["refresh_token"])

        
        # Prepare the data dictionary for updating
        updated_raw_material_data = {
                "raw_material_id": str(uuid.uuid4()),
                "raw_material_name": request.raw_material_name,
                "raw_material_code": request.raw_material_code,
                "quantity": request.quantity,
                "reorder_level": request.reorder_level,
                "unit_cost": request.unit_cost,
                "category": request.category,
                "updated_by": str(request.updated_by),
                "updated_at": request.updated_at.isoformat() if request.updated_at else None
        }

        result = (
            auth_supabase.table("raw_materials").update(updated_raw_material_data).eq("raw_material_id", id).execute()
        )
        
        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Raw material with id: {id} not found")
        record = result.data[0]
        
        return record

    except Exception as error:
        print(f"======= {error}->->->")
        raise HTTPException(status_code=500, detail=str(error))
