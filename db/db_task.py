from fastapi import HTTPException, status
from routers.schemas import TaskBase
from fastapi.responses import JSONResponse
from datetime import datetime


def create_task(db, request: TaskBase, user: dict):
    user_check = db.table("users").select("id").eq("id", request.created_by).execute()
    
    responds_uuid = db.table("users").select("id, uid").eq("id", request.created_by).execute()
    
    if responds_uuid.data:
        user_uuid = responds_uuid.data[0]['uid']
        
    if not user_check.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {request.created_by} does not exist"
        )
        
    data = {
        "batch_id": request.batch_id,
        "task_name": request.task_name,
        "task_description": request.task_description,
        "status": request.status,
        "updated_at": datetime.now().isoformat(),
        "created_by": request.created_by,  # Must match existing users.id
        "user_id": user_uuid,
        "task_notes": request.task_notes
    }

    response = db.table("tasks").insert(data).execute()

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create task"
        )

    return response.data[0]





def get_all_task(db, batch_id: int):
    response = db.table("tasks").select("*").eq("batch_id", batch_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch tasks")
    tasks = response.data

    # Fetch batch to get created_by user id
    batch_response = db.table("batch").select("created_by").eq("id", batch_id).execute()
    if not batch_response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Batch with id: {batch_id} not found")
    created_by = batch_response.data[0]["created_by"]

    if created_by is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batch with id: {batch_id} has no valid creator"
        )

    # Fetch user to get username
    user_response = db.table('users').select("username").eq("id", created_by).execute()
    if not user_response.data:
        username = "Unknown"
    else:
        username = user_response.data[0].get("username", "Unknown")

    # Add username to tasks if missing and validate created_by
    for task in tasks:
        if not task.get("username"):
            task["username"] = username
        if task.get("created_by") is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Task with id {task.get('id')} has invalid created_by value"
            )

    return tasks


def delete(id: int, db):
    response = db.table("tasks").delete().eq("id", id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} not found")
    return JSONResponse(content={"message": f"Deleted: Task with id:{id}"})
