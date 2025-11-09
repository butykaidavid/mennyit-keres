"""
Statistics API Router
Fizetési statisztikák és elemzések
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..config.database import get_db
from ..services.statistics_service import StatisticsService

router = APIRouter()


@router.get("/salary")
async def get_salary_statistics(
    job_title: Optional[str] = None,
    location: Optional[str] = None,
    experience_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Fizetési statisztikák lekérése
    - Szűrhető munkakör, helyszín és tapasztalat szerint
    """
    stats_service = StatisticsService(db)
    
    stats = stats_service.get_salary_stats(
        job_title=job_title,
        location=location,
        experience_level=experience_level
    )
    
    return {
        "filters": {
            "job_title": job_title,
            "location": location,
            "experience_level": experience_level
        },
        "statistics": [stat.to_dict() for stat in stats]
    }


@router.get("/trending")
async def get_trending_jobs(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Legkeresettebb munkakörök
    """
    stats_service = StatisticsService(db)
    trending = stats_service.get_trending_jobs(limit=limit)
    
    return {
        "count": len(trending),
        "trending_jobs": trending
    }


@router.get("/locations")
async def get_location_statistics(db: Session = Depends(get_db)):
    """
    Helyszín szerinti statisztikák
    """
    stats_service = StatisticsService(db)
    location_stats = stats_service.get_location_statistics()
    
    return {
        "locations": location_stats
    }


@router.get("/salary-distribution")
async def get_salary_distribution(
    job_title: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Fizetési eloszlás
    """
    stats_service = StatisticsService(db)
    distribution = stats_service.get_salary_distribution(job_title=job_title)
    
    return {
        "job_title": job_title,
        "distribution": distribution
    }
