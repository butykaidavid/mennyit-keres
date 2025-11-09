"""
Admin Service
Admin funkciók business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict
from uuid import UUID
import logging

from ..models.job import Job

logger = logging.getLogger(__name__)


class AdminService:
    """Admin service osztály"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def trigger_scraping(self, portal: str):
        """Scraping feladat indítása"""
        # TODO: Celery task meghívása
        logger.info(f"Scraping triggered for portal: {portal}")
        # from scraper.tasks import scrape_portal
        # scrape_portal.delay(portal)
    
    def get_pending_jobs(self, skip: int = 0, limit: int = 20) -> List[Job]:
        """Ellenőrzésre váró állások"""
        return self.db.query(Job).filter(
            Job.verified == False,
            Job.active == True
        ).offset(skip).limit(limit).all()
    
    def count_pending_jobs(self) -> int:
        """Ellenőrzésre váró állások száma"""
        return self.db.query(Job).filter(
            Job.verified == False,
            Job.active == True
        ).count()
    
    def verify_job(self, job_id: UUID, verified: bool) -> Optional[Job]:
        """Állás megerősítése"""
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.verified = verified
            self.db.commit()
            self.db.refresh(job)
        return job
    
    def delete_job(self, job_id: UUID) -> bool:
        """Állás törlése"""
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.active = False
            self.db.commit()
            return True
        return False
    
    def get_dashboard_stats(self) -> Dict:
        """Dashboard statisztikák"""
        total_jobs = self.db.query(Job).filter(Job.active == True).count()
        verified_jobs = self.db.query(Job).filter(
            Job.active == True,
            Job.verified == True
        ).count()
        pending_jobs = self.count_pending_jobs()
        
        # Portálok szerinti bontás
        portal_stats = self.db.query(
            Job.source_portal,
            func.count(Job.id).label('count')
        ).filter(
            Job.active == True
        ).group_by(
            Job.source_portal
        ).all()
        
        return {
            "total_jobs": total_jobs,
            "verified_jobs": verified_jobs,
            "pending_jobs": pending_jobs,
            "verification_rate": round((verified_jobs / total_jobs * 100) if total_jobs > 0 else 0, 2),
            "portals": [
                {"portal": row.source_portal, "count": row.count}
                for row in portal_stats
            ]
        }
