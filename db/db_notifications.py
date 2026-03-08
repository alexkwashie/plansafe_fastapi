import uuid
from fastapi import HTTPException, status
from db.supabase_client import supabase


def create_notification(user_id: str, notification_type: str, message: str, entity_type: str = None, entity_id: str = None):
    """Create an in-app notification record."""
    try:
        data = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "entity_type": entity_type,
            "entity_id": entity_id,
        }
        result = supabase.table("notifications").insert(data).execute()
        if not result.data:
            print(f"[Notification] Failed to create notification for user {user_id}")
            return None
        return result.data[0]
    except Exception as error:
        print(f"[Notification] Error creating notification: {error}")
        return None


def get_notifications_for_user(user_id: str, offset: int = 0, limit: int = 20):
    """Get paginated notifications for a user."""
    count_response = (
        supabase.table("notifications")
        .select("*", count="exact")
        .eq("user_id", user_id)
        .limit(0)
        .execute()
    )
    total = count_response.count or 0

    response = (
        supabase.table("notifications")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or [], total


def mark_as_read(notification_id: uuid.UUID):
    """Mark a notification as read."""
    result = (
        supabase.table("notifications")
        .update({"read": True})
        .eq("notification_id", str(notification_id))
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return result.data[0]
