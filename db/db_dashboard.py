from fastapi import HTTPException
from db.supabase_client import supabase


def get_summary():
    """Get dashboard summary: active batches, overdue tasks, recent incidents, equipment status."""
    try:
        # Active batches (status = "in_progress")
        active_batches = (
            supabase.table("batch_table")
            .select("*", count="exact")
            .eq("batch_status", "in_progress")
            .limit(0)
            .execute()
        )
        active_batch_count = active_batches.count or 0

        # Overdue tasks: status not completed/skipped and end_time is in the past
        # We fetch all non-completed tasks and filter in Python since Supabase REST
        # doesn't support comparing columns to now() easily
        overdue_response = (
            supabase.table("task_table")
            .select("*", count="exact")
            .not_.is_("end_time", "null")
            .neq("status", "completed")
            .neq("status", "skipped")
            .lt("end_time", "now()")
            .limit(0)
            .execute()
        )
        overdue_task_count = overdue_response.count or 0

        # Recent incidents (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).isoformat()
        recent_incidents = (
            supabase.table("incidents")
            .select("*", count="exact")
            .gte("incident_created_at", thirty_days_ago)
            .limit(0)
            .execute()
        )
        recent_incident_count = recent_incidents.count or 0

        # Equipment status breakdown
        equipment = supabase.table("machinery").select("status").execute()
        status_counts = {"available": 0, "in_use": 0, "maintenance": 0, "out_of_service": 0}
        for item in (equipment.data or []):
            s = item.get("status", "available")
            if s in status_counts:
                status_counts[s] += 1

        return {
            "active_batch_count": active_batch_count,
            "overdue_task_count": overdue_task_count,
            "recent_incident_count": recent_incident_count,
            "equipment_status": status_counts,
        }

    except Exception as error:
        print(f"======= Dashboard summary error: {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_active_batches():
    """Get active batches with task completion percentage."""
    try:
        batches_response = (
            supabase.table("batch_table")
            .select("*")
            .eq("batch_status", "in_progress")
            .execute()
        )
        batches = batches_response.data or []

        result = []
        for batch in batches:
            batch_id = batch["batch_id"]

            # Get total tasks for this batch
            total_response = (
                supabase.table("task_table")
                .select("*", count="exact")
                .eq("batch_id", batch_id)
                .limit(0)
                .execute()
            )
            total_tasks = total_response.count or 0

            # Get completed tasks
            completed_response = (
                supabase.table("task_table")
                .select("*", count="exact")
                .eq("batch_id", batch_id)
                .eq("status", "completed")
                .limit(0)
                .execute()
            )
            completed_tasks = completed_response.count or 0

            completion_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

            result.append({
                "batch_id": batch_id,
                "batch_title": batch.get("batch_title"),
                "batch_status": batch.get("batch_status"),
                "start_date": batch.get("start_date"),
                "end_date": batch.get("end_date"),
                "priority": batch.get("priority"),
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_percentage": round(completion_pct, 1),
            })

        return result

    except Exception as error:
        print(f"======= Active batches error: {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_overdue_tasks():
    """Get tasks that are past their end_time and not completed."""
    try:
        response = (
            supabase.table("task_table")
            .select("task_id, batch_id, task_name, status, end_time, sequence_order")
            .not_.is_("end_time", "null")
            .neq("status", "completed")
            .neq("status", "skipped")
            .lt("end_time", "now()")
            .order("end_time", desc=False)
            .execute()
        )
        return response.data or []

    except Exception as error:
        print(f"======= Overdue tasks error: {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_recent_incidents(limit: int = 10):
    """Get the most recent incidents."""
    try:
        response = (
            supabase.table("incidents")
            .select("*")
            .order("incident_created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data or []

    except Exception as error:
        print(f"======= Recent incidents error: {error}")
        raise HTTPException(status_code=500, detail=str(error))
