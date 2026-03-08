from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import IncidentBase, IncidentUpdate, IncidentDisplay
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_incident import db_incident
from db import db_notifications
from notifications.email import send_incident_notification_email
import uuid


router = APIRouter(
    prefix='/api/v1',
    tags=['incidents']
)


@router.post('/tasks/{task_id}/incidents', response_model=IncidentDisplay)
async def create(request: IncidentBase, task_id: uuid.UUID, background_tasks: BackgroundTasks, user=Depends(get_current_user)):
    result = db_incident.create_incident(request, user, task_id)

    # In-app notification for the creating user
    user_id = user.get("user_id") if isinstance(user, dict) else None
    if user_id:
        db_notifications.create_notification(
            user_id=user_id,
            notification_type="incident_created",
            message=f"Incident reported: {request.incident_name}",
            entity_type="incident",
            entity_id=result.get("incident_id"),
        )

    # Email safety officers in background
    severity = request.incident_severity.value if request.incident_severity else "unknown"
    background_tasks.add_task(
        send_incident_notification_email,
        request.incident_name,
        severity,
        request.location,
    )

    return result


@router.get('/incidents')
async def all_incidents_global(pagination: PaginationParams = Depends()):
    """List all incidents across all tasks (paginated)."""
    data, total = db_incident.get_all_incidents_global(offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/tasks/{task_id}/incidents')
async def all_incidents_by_task(task_id: uuid.UUID, pagination: PaginationParams = Depends()):
    data, total = db_incident.get_all_incident(task_id, offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/incidents/{incident_id}', response_model=IncidentDisplay)
async def get_incident_by_id(incident_id: uuid.UUID):
    return db_incident.get_by_id(incident_id)


@router.put('/incidents/{incident_id}', response_model=IncidentDisplay)
async def update(incident_id: uuid.UUID, request: IncidentUpdate, user=Depends(get_current_user)):
    return db_incident.update_incident(incident_id, request, user)


@router.delete('/incidents/{incident_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(incident_id: uuid.UUID, user=Depends(get_current_user)):
    if not db_incident.delete(incident_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
