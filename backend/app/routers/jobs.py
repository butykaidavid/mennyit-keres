"""
Jobs API Router
Állások kezelése - CRUD műveletek, keresés, szűrés
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..config.database import get_db
from ..models.job import Job
from ..services.job_service import JobService

router = APIRouter()


@router.get("/")
async def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    location: Optional[str] = None,
    category_id: Optional[UUID] = None,
    min_salary: Optional[int] = None,
    verified_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    Állások listázása
    - Paginálás: skip és limit paraméterekkel
    - Szűrés: helyszín, kategória, fizetés szerint
    """
    job_service = JobService(db)
    
    filters = {
        "location": location,
        "category_id": category_id,
        "min_salary": min_salary,
        "verified_only": verified_only
    }
    
    jobs = job_service.get_jobs(skip=skip, limit=limit, filters=filters)
    total = job_service.count_jobs(filters=filters)
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "jobs": [job.to_dict() for job in jobs]
    }


@router.get("/{job_id}")
async def get_job(job_id: UUID, db: Session = Depends(get_db)):
    """
    Egy állás részletes adatai
    """
    job_service = JobService(db)
    job = job_service.get_job_by_id(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Állás nem található")
    
    return job.to_dict()


@router.get("/search/")
async def search_jobs(
    q: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Állások keresése kulcsszavak alapján
    - Keres a cím, leírás és készségek között
    """
    job_service = JobService(db)
    jobs = job_service.search_jobs(query=q, skip=skip, limit=limit)
    total = job_service.count_search_results(query=q)
    
    return {
        "query": q,
        "total": total,
        "skip": skip,
        "limit": limit,
        "jobs": [job.to_dict() for job in jobs]
    }


@router.get("/by-title/{title}")
async def get_jobs_by_title(
    title: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Állások egy adott címmel
    """
    job_service = JobService(db)
    jobs = job_service.get_jobs_by_title(title=title, skip=skip, limit=limit)
    
    return {
        "title": title,
        "count": len(jobs),
        "jobs": [job.to_dict() for job in jobs]
    }


@router.post("/")
async def create_job(job_data: dict, db: Session = Depends(get_db)):
    """
    Új állás létrehozása
    (Admin funkció)
    """
    job_service = JobService(db)
    job = job_service.create_job(job_data)
    
    return {
        "message": "Állás sikeresen létrehozva",
        "job": job.to_dict()
    }
