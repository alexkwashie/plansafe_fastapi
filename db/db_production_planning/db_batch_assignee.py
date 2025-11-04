from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from supabase import create_client
import os
import uuid
from dotenv import load_dotenv
import os

# Load .env file (for local development)
load_dotenv()

# Load environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Basic validation
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
from dotenv import load_dotenv


# Load .env file (for local development)
load_dotenv()

# Load environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Basic validation
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")

# Create Supabase client (URL first, then key)
auth_supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_batch_assignees(batch_id: uuid.UUID, user_id: uuid.UUID, user: dict = None):
    try:
        # Create Supabase client with the user's token
        if user and "access_token" in user and "refresh_token" in user:
            auth_supabase.auth.set_session(
                user["access_token"], user["refresh_token"]
            )

        # Prepare the data dictionary for insertion
        batch_assignee_data = {
            "batch_id": str(batch_id),
            "user_id": str(user_id)
    
        }

        result = (
            auth_supabase.table("batch_assignees").insert(batch_assignee_data).execute()
        )
        

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create task"
            )

        return result.data[0]

    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))





def get_all_batch_assignee(batch_id: uuid.UUID):
    response = auth_supabase.table("batch_assignees").select("*").eq("batch_id", batch_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch tasks")
    
    batchs_assignee = response.data
    
    #print(tasks_assignee)
    
    return batchs_assignee
    



def delete(assignees_id: uuid.UUID, db):
    response = db.table("batch_assignees").delete().eq("batch_assignees_id", assignees_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Task assignee with id:{assignees_id}"})
