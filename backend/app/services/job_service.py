"""
Job Service
Állásokkal kapcsolatos business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional, Dict
from uuid import UUID

from ..models.job import Job


class JobService:
    """Job service osztály"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_jobs(self, skip: int = 0, limit: int = 10, filters: Dict = None) -> List[Job]:
        """Állások listázása szűrőkkel"""
        query = self.db.query(Job).filter(Job.active == True)
        
        if filters:
            if filters.get("location"):
                query = query.filter(Job.location.ilike(f"%{filters['location']}%"))
            
            if filters.get("category_id"):
                query = query.filter(Job.category_id == filters["category_id"])
            
            if filters.get("min_salary"):
                query = query.filter(Job.salary_min >= filters["min_salary"])
            
            if filters.get("verified_only"):
                query = query.filter(Job.verified == True)
        
        return query.order_by(Job.created_at.desc()).offset(skip).limit(limit).all()
    
    def count_jobs(self, filters: Dict = None) -> int:
        """Állások számának lekérdezése"""
        query = self.db.query(Job).filter(Job.active == True)
        
        if filters:
            if filters.get("location"):
                query = query.filter(Job.location.ilike(f"%{filters['location']}%"))
            
            if filters.get("category_id"):
                query = query.filter(Job.category_id == filters["category_id"])
            
            if filters.get("min_salary"):
                query = query.filter(Job.salary_min >= filters["min_salary"])
            
            if filters.get("verified_only"):
                query = query.filter(Job.verified == True)
        
        return query.count()
    
    def get_job_by_id(self, job_id: UUID) -> Optional[Job]:
        """Állás lekérése ID alapján"""
        return self.db.query(Job).filter(Job.id == job_id).first()
    
    def search_jobs(self, query: str, skip: int = 0, limit: int = 10) -> List[Job]:
        """Állások keresése"""
        search_pattern = f"%{query}%"
        
        return self.db.query(Job).filter(
            and_(
                Job.active == True,
                or_(
                    Job.title.ilike(search_pattern),
                    Job.description.ilike(search_pattern),
                    Job.company.ilike(search_pattern)
                )
            )
        ).offset(skip).limit(limit).all()
    
    def count_search_results(self, query: str) -> int:
        """Keresési találatok száma"""
        search_pattern = f"%{query}%"
        
        return self.db.query(Job).filter(
            and_(
                Job.active == True,
                or_(
                    Job.title.ilike(search_pattern),
                    Job.description.ilike(search_pattern),
                    Job.company.ilike(search_pattern)
                )
            )
        ).count()
    
    def get_jobs_by_title(self, title: str, skip: int = 0, limit: int = 10) -> List[Job]:
        """Állások lekérése cím alapján"""
        return self.db.query(Job).filter(
            and_(
                Job.active == True,
                Job.title.ilike(f"%{title}%")
            )
        ).offset(skip).limit(limit).all()
    
    def create_job(self, job_data: Dict) -> Job:
        """Új állás létrehozása"""
        job = Job(**job_data)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job
    
    def update_job(self, job_id: UUID, job_data: Dict) -> Optional[Job]:
        """Állás frissítése"""
        job = self.get_job_by_id(job_id)
        if job:
            for key, value in job_data.items():
                setattr(job, key, value)
            self.db.commit()
            self.db.refresh(job)
        return job
    
    def delete_job(self, job_id: UUID) -> bool:
        """Állás törlése (soft delete)"""
        job = self.get_job_by_id(job_id)
        if job:
            job.active = False
            self.db.commit()
            return True
        return False
