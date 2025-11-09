"""
Categories API Router
Kategóriák kezelése
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from ..config.database import get_db
from ..services.category_service import CategoryService

router = APIRouter()


@router.get("/")
async def get_categories(db: Session = Depends(get_db)):
    """
    Összes kategória listázása
    """
    category_service = CategoryService(db)
    categories = category_service.get_all_categories()
    
    return {
        "total": len(categories),
        "categories": [cat.to_dict() for cat in categories]
    }


@router.get("/{slug}")
async def get_category(slug: str, db: Session = Depends(get_db)):
    """
    Egy kategória részletei slug alapján
    """
    category_service = CategoryService(db)
    category = category_service.get_category_by_slug(slug)
    
    if not category:
        raise HTTPException(status_code=404, detail="Kategória nem található")
    
    # Kategória állásainak száma
    job_count = category_service.get_job_count_for_category(category.id)
    
    result = category.to_dict()
    result["job_count"] = job_count
    
    return result


@router.get("/{slug}/jobs")
async def get_category_jobs(
    slug: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Egy kategória állásai
    """
    category_service = CategoryService(db)
    category = category_service.get_category_by_slug(slug)
    
    if not category:
        raise HTTPException(status_code=404, detail="Kategória nem található")
    
    jobs = category_service.get_jobs_for_category(category.id, skip, limit)
    total = category_service.get_job_count_for_category(category.id)
    
    return {
        "category": category.to_dict(),
        "total": total,
        "jobs": [job.to_dict() for job in jobs]
    }
