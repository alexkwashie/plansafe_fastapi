from fastapi import HTTPException
from db.supabase_client import supabase


def get_incidents_for_year(year: int):
    """Fetch all incidents for a given year based on date_of_injury."""
    start = f"{year}-01-01"
    end = f"{year}-12-31"

    response = (
        supabase.table("incidents")
        .select("*")
        .gte("date_of_injury", start)
        .lte("date_of_injury", end)
        .order("date_of_injury", desc=False)
        .execute()
    )
    return response.data or []


def generate_osha_300(year: int):
    """Generate OSHA 300 Log data — Log of Work-Related Injuries and Illnesses."""
    incidents = get_incidents_for_year(year)

    log_entries = []
    for i, inc in enumerate(incidents, start=1):
        log_entries.append({
            "case_number": i,
            "employee_name": inc.get("employee_name", ""),
            "job_title": inc.get("job_title_at_time", ""),
            "date_of_injury": inc.get("date_of_injury", ""),
            "location": inc.get("location", ""),
            "description": inc.get("injury_description") or inc.get("incident_notes", ""),
            "injury_type": inc.get("injury_type", ""),
            "body_part_affected": inc.get("body_part_affected", ""),
            "death": inc.get("death", False),
            "days_away": inc.get("days_away", 0),
            "days_restricted": inc.get("days_restricted", 0),
            "treated_in_er": inc.get("treated_in_er", False),
            "hospitalized": inc.get("hospitalized", False),
        })

    return {
        "year": year,
        "total_cases": len(log_entries),
        "entries": log_entries,
    }


def generate_osha_300a(year: int):
    """Generate OSHA 300A Summary — Summary of Work-Related Injuries and Illnesses."""
    incidents = get_incidents_for_year(year)

    total_cases = len(incidents)
    total_deaths = sum(1 for i in incidents if i.get("death"))
    total_days_away_cases = sum(1 for i in incidents if (i.get("days_away") or 0) > 0)
    total_days_away = sum(i.get("days_away", 0) or 0 for i in incidents)
    total_restricted_cases = sum(1 for i in incidents if (i.get("days_restricted") or 0) > 0)
    total_days_restricted = sum(i.get("days_restricted", 0) or 0 for i in incidents)
    total_other_cases = total_cases - total_deaths - total_days_away_cases - total_restricted_cases

    # Injury type breakdown
    injury_types = {}
    for inc in incidents:
        itype = inc.get("injury_type", "other") or "other"
        injury_types[itype] = injury_types.get(itype, 0) + 1

    return {
        "year": year,
        "total_cases": total_cases,
        "total_deaths": total_deaths,
        "total_days_away_cases": total_days_away_cases,
        "total_days_away": total_days_away,
        "total_restricted_cases": total_restricted_cases,
        "total_days_restricted": total_days_restricted,
        "total_other_cases": max(total_other_cases, 0),
        "injury_type_breakdown": injury_types,
    }


def generate_osha_301(incident_id: str):
    """Generate OSHA 301 — Injury and Illness Incident Report for a specific incident."""
    response = supabase.table("incidents").select("*").eq("incident_id", incident_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Incident not found")

    inc = response.data[0]

    return {
        "case_number": inc.get("incident_id"),
        "employee_name": inc.get("employee_name", ""),
        "job_title": inc.get("job_title_at_time", ""),
        "date_of_injury": inc.get("date_of_injury", ""),
        "time_of_event": inc.get("incident_time", ""),
        "location": inc.get("location", ""),
        "description_of_injury": inc.get("injury_description") or inc.get("incident_notes", ""),
        "body_part_affected": inc.get("body_part_affected", ""),
        "object_or_substance": inc.get("injury_type", ""),
        "death": inc.get("death", False),
        "days_away": inc.get("days_away", 0),
        "days_restricted": inc.get("days_restricted", 0),
        "treated_in_er": inc.get("treated_in_er", False),
        "hospitalized": inc.get("hospitalized", False),
        "severity": inc.get("incident_severity", ""),
        "witness_info": inc.get("witness_info", ""),
        "immediate_actions": inc.get("immediate_actions", ""),
    }
