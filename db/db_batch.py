from fastapi import HTTPException, status, Depends
from routers.schemas import BatchBase
from fastapi.responses import JSONResponse


def create_batch(db, request: BatchBase):
    # Check if user exists
    user_check = db.table("users").select("id").eq("id", request.created_by).execute()
    if not user_check.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {request.created_by} does not exist"
        )

    # Convert datetime to ISO format if needed
    start_date = request.start_date.isoformat() if hasattr(request.start_date, "isoformat") else request.start_date
    end_date = request.end_date.isoformat() if hasattr(request.end_date, "isoformat") else request.end_date

    # Prepare data
    data = {
        "batch_title": request.batch_title,
        "color_tag": request.color_tag,
        "start_date": start_date,
        "end_date": end_date,
        "created_by": request.created_by,
        "description": request.description
    }

    # Insert into Supabase
    response = db.table("batch").insert(data).execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create batch"
        )

    return response.data[0]



def get_all(db):
    response = db.table("batch").select("*").execute()


    # Safely handle empty or invalid response
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No batch data returned"
        )

    batches = response.data

    # Fetch users
    user_response = db.table("users").select("id, username").execute()
    if not user_response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user data returned"
        )

    users = {user["id"]: user["username"] for user in user_response.data}

    # Enrich tasks
    for batch in batches:
        if "tasks" in batch:
            for task in batch["tasks"]:
                if not task.get("username"):
                    task["username"] = users.get(batch["created_by"], "Unknown")

    return batches



def delete(id: int, db):
    response = db.table("batch").delete().eq("id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Batch with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Batch with id:{id}"})
