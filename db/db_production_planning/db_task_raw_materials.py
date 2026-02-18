from fastapi import HTTPException, status
from routers.schemas import TaskRawMaterialBase
from fastapi.responses import JSONResponse
import uuid
from db.supabase_client import supabase


def create_task_raw_material(request: TaskRawMaterialBase, task_id: uuid.UUID, raw_material_id: uuid.UUID, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        raw_material_response = supabase.table("raw_materials").select("*").eq("raw_material_id", str(raw_material_id)).execute()
        if not raw_material_response.data:
            raise HTTPException(status_code=404, detail=f"Raw material with id: {raw_material_id} not found")
        raw_material_item = raw_material_response.data[0]

        task_raw_material_data = {
            "task_id": str(task_id),
            "raw_material_id": str(raw_material_id),
            "material_name": raw_material_item.get("raw_material_name"),
            "assigned_quantity": request.assigned_quantity
        }

        result = (supabase.table("task_raw_materials").insert(task_raw_material_data).execute())

        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create task raw material")

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all_task_raw_material(task_id: uuid.UUID, offset: int = 0, limit: int = 20):
    count_response = (
        supabase.table("task_raw_materials")
        .select("*", count="exact")
        .eq("task_id", str(task_id))
        .limit(0)
        .execute()
    )
    total = count_response.count or 0

    response = (
        supabase.table("task_raw_materials")
        .select("*")
        .eq("task_id", str(task_id))
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or [], total


def delete(id: uuid.UUID):
    response = supabase.table("task_raw_materials").delete().eq("task_raw_material_id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task raw material with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Task raw material with id:{id}"})
