import uuid
from fastapi import HTTPException, status
from routers.schemas import MachineryBase, MachineryBaseUpdate
from fastapi.responses import JSONResponse
from db.supabase_client import supabase


def create_machinery(request: MachineryBase, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        result = (
            supabase.table("machinery")
            .insert({
                "machine_name": request.machine_name,
                "machine_type": request.machine_type,
                "machine_manufacture": request.machine_manufacture,
                "location": request.location,
                "status": request.status.value if request.status else "available",
                "capacity": request.capacity,
                "power_rating": request.power_rating,
                "serial_number": request.serial_number,
                "purchase_date": request.purchase_date.isoformat() if request.purchase_date else None,
                "warranty_expiry": request.warranty_expiry.isoformat() if request.warranty_expiry else None,
                "photo_url": request.photo_url,
                "notes": request.notes,
                "created_at": request.created_at.isoformat() if request.created_at else None,
                "created_by": str(request.created_by) if request.created_by else None,
            })
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add machinery"
            )

        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all_machinery(offset: int = 0, limit: int = 20):
    count_response = supabase.table("machinery").select("*", count="exact").limit(0).execute()
    total = count_response.count or 0

    response = supabase.table("machinery").select("*").range(offset, offset + limit - 1).execute()
    return response.data or [], total


def get_by_id(machinery_id: uuid.UUID):
    response = supabase.table("machinery").select("*").eq("machinery_id", str(machinery_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machinery not found")
    return response.data[0]


def delete(id: uuid.UUID):
    response = supabase.table("machinery").delete().eq("machinery_id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machinery with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Machinery with id:{id}"})


def update_machinery(id: uuid.UUID, request: MachineryBaseUpdate, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        updated_machinery_data = {
                "machine_name": request.machine_name,
                "machine_type": request.machine_type,
                "machine_manufacture": request.machine_manufacture,
                "location": request.location,
                "status": request.status.value if request.status else "available",
                "capacity": request.capacity,
                "power_rating": request.power_rating,
                "serial_number": request.serial_number,
                "purchase_date": request.purchase_date.isoformat() if request.purchase_date else None,
                "warranty_expiry": request.warranty_expiry.isoformat() if request.warranty_expiry else None,
                "photo_url": request.photo_url,
                "notes": request.notes,
                "updated_by": str(request.updated_by) if request.updated_by else None,
                "updated_at": request.updated_at.isoformat() if request.updated_at else None,
        }

        result = (
            supabase.table("machinery").update(updated_machinery_data).eq("machinery_id", id).execute()
        )

        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machinery with id: {id} not found")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}->->->")
        raise HTTPException(status_code=500, detail=str(error))
