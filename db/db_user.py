from fastapi import HTTPException, status
import uuid
from db.supabase_client import supabase


def get_all_users(offset: int = 0, limit: int = 20):
    count_response = supabase.table("users").select("*", count="exact").limit(0).execute()
    total = count_response.count or 0

    response = supabase.table("users").select("*").range(offset, offset + limit - 1).execute()
    if not response.data:
        return [], total

    users = [{
        "username": str(user.get("username")),
        "firstname": str(user.get("firstName")),
        "lastname": str(user.get("lastName")),
        "email": str(user.get("email")),
        "uid": str(user.get("uid"))
    } for user in response.data]

    return users, total


def get_current_user(uid: uuid.UUID):
    try:
        response = supabase.table("users").select("*").eq("uid", str(uid)).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user_data = response.data[0]

        return {
            "username": user_data.get("username"),
            "firstname": user_data.get("firstName"),
            "lastname": user_data.get("lastName"),
            "email": user_data.get("email"),
            "uid": user_data.get("uid"),
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
