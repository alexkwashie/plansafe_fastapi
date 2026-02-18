import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import TaskAssigneeBase, TaskAssigneeDisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_production_planning import db_task_assignee
from db.db_production_planning import db_task
from db import db_notifications
from db.supabase_client import supabase
from notifications.email import send_task_assignment_email


router = APIRouter(
    prefix='/api/v1',
    tags=['task-assignees']
)


@router.post('/tasks/{task_id}/assignees', response_model=TaskAssigneeDisplay)
async def create(request: TaskAssigneeBase, task_id: uuid.UUID, background_tasks: BackgroundTasks, user=Depends(get_current_user)):
    result = db_task_assignee.create_task_assignees(task_id, request.user_id, request)

    # Send notification and email in background
    if request.user_id:
        task_info = db_task.get_by_id(task_id)
        task_name = task_info.get("task_name", "Unknown Task")
        batch_id = task_info.get("batch_id", "")

        # In-app notification
        db_notifications.create_notification(
            user_id=str(request.user_id),
            notification_type="task_assignment",
            message=f"You have been assigned to task: {task_name}",
            entity_type="task",
            entity_id=str(task_id),
        )

        # Email notification (background)
        user_response = supabase.table("users").select("email").eq("uid", str(request.user_id)).execute()
        if user_response.data:
            assignee_email = user_response.data[0].get("email")
            if assignee_email:
                batch_title = batch_id  # fallback
                background_tasks.add_task(send_task_assignment_email, assignee_email, task_name, str(batch_title))

    return result


@router.get('/tasks/{task_id}/assignees')
async def list_task_assignees(task_id: uuid.UUID, pagination: PaginationParams = Depends()):
    data, total = db_task_assignee.get_all_task_assignee(task_id, offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.delete('/task-assignees/{assignee_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(assignee_id: uuid.UUID, user=Depends(get_current_user)):
    """Delete a task assignee by its ID."""
    if not db_task_assignee.delete(assignee_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task assignee not found")
