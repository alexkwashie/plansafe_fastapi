import uuid
from fastapi import HTTPException, status
from routers.schemas import ChecklistTemplateBase, ChecklistTemplateUpdate, TemplateItemBase
from db.supabase_client import supabase


def create_template(request: ChecklistTemplateBase, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        data = {
            "name": request.name,
            "type": request.type.value if request.type else "pre_shift",
            "created_by": user.get("user_id") if user else None,
        }

        result = supabase.table("checklist_templates").insert(data).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create template")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all_templates(offset: int = 0, limit: int = 20):
    count_response = supabase.table("checklist_templates").select("*", count="exact").limit(0).execute()
    total = count_response.count or 0

    response = (
        supabase.table("checklist_templates")
        .select("*")
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or [], total


def get_by_id(template_id: uuid.UUID):
    response = supabase.table("checklist_templates").select("*").eq("template_id", str(template_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    return response.data[0]


def update_template(template_id: uuid.UUID, request: ChecklistTemplateUpdate, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        update_data = {}
        if request.name is not None:
            update_data["name"] = request.name
        if request.type is not None:
            update_data["type"] = request.type.value

        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        result = supabase.table("checklist_templates").update(update_data).eq("template_id", str(template_id)).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def delete_template(template_id: uuid.UUID):
    response = supabase.table("checklist_templates").delete().eq("template_id", str(template_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    return True


# Template items
def add_item(template_id: uuid.UUID, request: TemplateItemBase):
    try:
        data = {
            "template_id": str(template_id),
            "item_text": request.item_text,
            "sort_order": request.sort_order,
            "required": request.required,
        }
        result = supabase.table("checklist_template_items").insert(data).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to add item")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_items(template_id: uuid.UUID):
    response = (
        supabase.table("checklist_template_items")
        .select("*")
        .eq("template_id", str(template_id))
        .order("sort_order", desc=False)
        .execute()
    )
    return response.data or []


def delete_item(item_id: uuid.UUID):
    response = supabase.table("checklist_template_items").delete().eq("item_id", str(item_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template item not found")
    return True
