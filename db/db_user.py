from fastapi import HTTPException, status
from routers.schemas import MachineryBase
from fastapi.responses import JSONResponse
from supabase import create_client
import os
import uuid

auth_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def get_all_users():
    response = auth_supabase.table("users").select("*").execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch machinery data")
    users = response.data  # Get all user records
    print("Retrieved users:", users)  # Debug statement

    return [{
        "username": str(user.get("username")),
        "email": str(user.get("email")),
        "uid": str(user.get("uid"))
    } for user in users]  # Return a list of user dictionaries


def get_current_user(uid: uuid.UUID):
    try:
        response = auth_supabase.table("users").select("*").eq("uid", str(uid)).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch tasks")
        user_data = response.data[0]  # Get the first user record
        
        return {
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "uid": user_data.get("uid"),
            # Add any other fields you need
        }
        
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))
