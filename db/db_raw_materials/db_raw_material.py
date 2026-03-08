import uuid
from fastapi import HTTPException, status
from routers.schemas import RawMaterialBase, RawMaterialUpdate
from fastapi.responses import JSONResponse
from db.supabase_client import supabase


def create_raw_material(request: RawMaterialBase, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        result = (
            supabase.table("raw_materials").insert({
                "raw_material_name": request.raw_material_name,
                "raw_material_code": request.raw_material_code,
                "quantity": request.quantity,
                "reorder_level": request.reorder_level,
                "unit_cost": request.unit_cost,
                "category": request.category,
                "supplier": request.supplier,
                "unit_of_measure": request.unit_of_measure,
                "lot_number": request.lot_number,
                "created_at": request.created_at.isoformat() if request.created_at else None,
                "created_by": str(request.created_by) if request.created_by else None,
            })
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add raw material"
            )

        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all_raw_material(offset: int = 0, limit: int = 20):
    count_response = supabase.table("raw_materials").select("*", count="exact").limit(0).execute()
    total = count_response.count or 0

    response = supabase.table("raw_materials").select("*").range(offset, offset + limit - 1).execute()
    return response.data or [], total


def get_by_id(raw_material_id: uuid.UUID):
    response = supabase.table("raw_materials").select("*").eq("raw_material_id", str(raw_material_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raw material not found")
    return response.data[0]


def delete(id: uuid.UUID):
    response = supabase.table("raw_materials").delete().eq("raw_material_id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Raw material with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Raw material with id:{id}"})


def update_raw_material(id: uuid.UUID, request: RawMaterialUpdate, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        updated_raw_material_data = {
                "raw_material_name": request.raw_material_name,
                "raw_material_code": request.raw_material_code,
                "quantity": request.quantity,
                "reorder_level": request.reorder_level,
                "unit_cost": request.unit_cost,
                "category": request.category,
                "supplier": request.supplier,
                "unit_of_measure": request.unit_of_measure,
                "lot_number": request.lot_number,
                "updated_by": str(request.updated_by) if request.updated_by else None,
                "updated_at": request.updated_at.isoformat() if request.updated_at else None,
        }

        result = (
            supabase.table("raw_materials").update(updated_raw_material_data).eq("raw_material_id", id).execute()
        )

        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Raw material with id: {id} not found")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}->->->")
        raise HTTPException(status_code=500, detail=str(error))
