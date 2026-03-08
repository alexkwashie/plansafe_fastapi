from fastapi import APIRouter, Query
from fastapi.responses import Response
from reports.osha_generator import generate_osha_300, generate_osha_300a, generate_osha_301
from reports.pdf_generator import generate_osha_300_pdf, generate_osha_300a_pdf, generate_osha_301_pdf
import uuid


router = APIRouter(
    prefix='/api/v1/reports',
    tags=['reports']
)


@router.get('/osha-300')
async def osha_300(year: int = Query(..., description="Year for OSHA 300 log"), format: str = Query("json", description="Output format: json or pdf")):
    """Generate OSHA 300 Log — Log of Work-Related Injuries and Illnesses."""
    data = generate_osha_300(year)

    if format == "pdf":
        pdf_bytes = generate_osha_300_pdf(data)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=osha_300_{year}.pdf"},
        )

    return data


@router.get('/osha-300a')
async def osha_300a(year: int = Query(..., description="Year for OSHA 300A summary"), format: str = Query("json", description="Output format: json or pdf")):
    """Generate OSHA 300A Summary — Summary of Work-Related Injuries and Illnesses."""
    data = generate_osha_300a(year)

    if format == "pdf":
        pdf_bytes = generate_osha_300a_pdf(data)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=osha_300a_{year}.pdf"},
        )

    return data


@router.get('/osha-301/{incident_id}')
async def osha_301(incident_id: uuid.UUID, format: str = Query("json", description="Output format: json or pdf")):
    """Generate OSHA 301 — Injury and Illness Incident Report for a specific incident."""
    data = generate_osha_301(str(incident_id))

    if format == "pdf":
        pdf_bytes = generate_osha_301_pdf(data)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=osha_301_{incident_id}.pdf"},
        )

    return data
