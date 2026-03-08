from fastapi import APIRouter, Query
from routers.schemas import DashboardSummary, ActiveBatchSummary, OverdueTask
from db import db_dashboard
from typing import List


router = APIRouter(
    prefix='/api/v1/dashboard',
    tags=['dashboard']
)


@router.get('/summary', response_model=DashboardSummary)
async def summary():
    """Dashboard summary: active batch count, overdue tasks, recent incidents, equipment status."""
    return db_dashboard.get_summary()


@router.get('/active-batches', response_model=List[ActiveBatchSummary])
async def active_batches():
    """Active batches with task completion percentage."""
    return db_dashboard.get_active_batches()


@router.get('/overdue-tasks', response_model=List[OverdueTask])
async def overdue_tasks():
    """Tasks past their end_time that aren't completed."""
    return db_dashboard.get_overdue_tasks()


@router.get('/recent-incidents')
async def recent_incidents(limit: int = Query(10, ge=1, le=50)):
    """Most recent incidents (default 10)."""
    return db_dashboard.get_recent_incidents(limit=limit)
