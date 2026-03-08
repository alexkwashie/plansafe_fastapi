from fastapi import HTTPException, status
from routers.schemas import IncidentBase, IncidentUpdate
from fastapi.responses import JSONResponse
import uuid
from db.supabase_client import supabase


def create_incident(request: IncidentBase, user, task_id: uuid.UUID):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        incident_data = {
            "task_incident_id": str(task_id),
            "incident_name": request.incident_name,
            "incident_type": request.incident_type,
            "incident_video_id": str(request.incident_video_id) if request.incident_video_id else None,
            "incident_voice_id": str(request.incident_voice_id) if request.incident_voice_id else None,
            "incident_photo_id": str(request.incident_photo_id) if request.incident_photo_id else None,
            "incident_time": request.incident_time.isoformat() if request.incident_time else None,
            "incident_notes": request.incident_notes,
            "incident_severity": request.incident_severity.value if request.incident_severity else None,
            "location": request.location,
            "personnel_involved": request.personnel_involved,
            "immediate_actions": request.immediate_actions,
            "witness_info": request.witness_info,
            "is_anonymous": request.is_anonymous,
            "employee_name": request.employee_name,
            "job_title_at_time": request.job_title_at_time,
            "date_of_injury": request.date_of_injury.isoformat() if request.date_of_injury else None,
            "injury_description": request.injury_description,
            "body_part_affected": request.body_part_affected,
            "injury_type": request.injury_type,
            "days_away": request.days_away,
            "days_restricted": request.days_restricted,
            "death": request.death,
            "treated_in_er": request.treated_in_er,
            "hospitalized": request.hospitalized,
        }

        result = (
            supabase.table("incidents").insert(incident_data).execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create incident"
            )

        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_all_incident(task_id: uuid.UUID, offset: int = 0, limit: int = 20):
    count_response = (
        supabase.table("incidents")
        .select("*", count="exact")
        .eq("task_incident_id", str(task_id))
        .limit(0)
        .execute()
    )
    total = count_response.count or 0

    response = (
        supabase.table("incidents")
        .select("*")
        .eq("task_incident_id", str(task_id))
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or [], total


def get_all_incidents_global(offset: int = 0, limit: int = 20):
    count_response = (
        supabase.table("incidents")
        .select("*", count="exact")
        .limit(0)
        .execute()
    )
    total = count_response.count or 0

    response = (
        supabase.table("incidents")
        .select("*")
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or [], total


def get_by_id(incident_id: uuid.UUID):
    response = supabase.table("incidents").select("*").eq("incident_id", str(incident_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return response.data[0]


def update_incident(incident_id: uuid.UUID, request: IncidentUpdate, user: dict = None):
    try:
        if user and "access_token" in user and "refresh_token" in user:
            supabase.auth.set_session(user["access_token"], user["refresh_token"])

        update_data = {}
        if request.incident_name is not None:
            update_data["incident_name"] = request.incident_name
        if request.incident_type is not None:
            update_data["incident_type"] = request.incident_type
        if request.incident_video_id is not None:
            update_data["incident_video_id"] = str(request.incident_video_id)
        if request.incident_voice_id is not None:
            update_data["incident_voice_id"] = str(request.incident_voice_id)
        if request.incident_photo_id is not None:
            update_data["incident_photo_id"] = str(request.incident_photo_id)
        if request.incident_time is not None:
            update_data["incident_time"] = request.incident_time.isoformat()
        if request.incident_notes is not None:
            update_data["incident_notes"] = request.incident_notes
        if request.incident_severity is not None:
            update_data["incident_severity"] = request.incident_severity.value
        if request.location is not None:
            update_data["location"] = request.location
        if request.personnel_involved is not None:
            update_data["personnel_involved"] = request.personnel_involved
        if request.immediate_actions is not None:
            update_data["immediate_actions"] = request.immediate_actions
        if request.witness_info is not None:
            update_data["witness_info"] = request.witness_info
        if request.is_anonymous is not None:
            update_data["is_anonymous"] = request.is_anonymous
        if request.employee_name is not None:
            update_data["employee_name"] = request.employee_name
        if request.job_title_at_time is not None:
            update_data["job_title_at_time"] = request.job_title_at_time
        if request.date_of_injury is not None:
            update_data["date_of_injury"] = request.date_of_injury.isoformat()
        if request.injury_description is not None:
            update_data["injury_description"] = request.injury_description
        if request.body_part_affected is not None:
            update_data["body_part_affected"] = request.body_part_affected
        if request.injury_type is not None:
            update_data["injury_type"] = request.injury_type
        if request.days_away is not None:
            update_data["days_away"] = request.days_away
        if request.days_restricted is not None:
            update_data["days_restricted"] = request.days_restricted
        if request.death is not None:
            update_data["death"] = request.death
        if request.treated_in_er is not None:
            update_data["treated_in_er"] = request.treated_in_er
        if request.hospitalized is not None:
            update_data["hospitalized"] = request.hospitalized

        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        result = supabase.table("incidents").update(update_data).eq("incident_id", str(incident_id)).execute()

        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incident with id: {incident_id} not found")
        return result.data[0]

    except HTTPException:
        raise
    except Exception as error:
        print(f"======= {error}")
        raise HTTPException(status_code=500, detail=str(error))


def delete(incident_id: uuid.UUID):
    response = supabase.table("incidents").delete().eq("incident_id", str(incident_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incident with id: {incident_id} not found")
    return JSONResponse(content={"message": f"Deleted: Incident with id:{incident_id}"})
