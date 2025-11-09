"""
Admin API Router
Admin funkciók - scraping kezelés, adatok moderálása
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import UUID

from ..config.database import get_db
from ..services.admin_service import AdminService

router = APIRouter()


@router.post("/scrape/trigger")
async def trigger_scraping(
    background_tasks: BackgroundTasks,
    portal: str = "all",
    db: Session = Depends(get_db)
):
    """
    Scraping feladat indítása
    - portal: profession, jobs, cvonline vagy all
    """
    admin_service = AdminService(db)
    
    # Background task-ként indítjuk
    background_tasks.add_task(admin_service.trigger_scraping, portal)
    
    return {
        "message": f"Scraping elindítva: {portal}",
        "status": "scheduled"
    }


@router.get("/jobs/pending")
async def get_pending_jobs(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Ellenőrzésre váró állások
    """
    admin_service = AdminService(db)
    jobs = admin_service.get_pending_jobs(skip=skip, limit=limit)
    total = admin_service.count_pending_jobs()
    
    return {
        "total": total,
        "jobs": [job.to_dict() for job in jobs]
    }


@router.put("/jobs/{job_id}/verify")
async def verify_job(
    job_id: UUID,
    verified: bool = True,
    db: Session = Depends(get_db)
):
    """
    Állás megerősítése/elutasítása
    """
    admin_service = AdminService(db)
    job = admin_service.verify_job(job_id, verified)
    
    if not job:
        raise HTTPException(status_code=404, detail="Állás nem található")
    
    return {
        "message": "Állás státusza frissítve",
        "job": job.to_dict()
    }


@router.delete("/jobs/{job_id}")
async def delete_job(job_id: UUID, db: Session = Depends(get_db)):
    """
    Állás törlése
    """
    admin_service = AdminService(db)
    success = admin_service.delete_job(job_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Állás nem található")
    
    return {
        "message": "Állás sikeresen törölve"
    }


@router.get("/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Admin dashboard statisztikák
    """
    admin_service = AdminService(db)
    stats = admin_service.get_dashboard_stats()
    
    return stats
