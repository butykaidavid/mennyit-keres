"""
Statistics Service
Statisztikai számításokkal kapcsolatos business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict

from ..models.job import Job
from ..models.salary_statistics import SalaryStatistics


class StatisticsService:
    """Statistics service osztály"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_salary_stats(
        self,
        job_title: Optional[str] = None,
        location: Optional[str] = None,
        experience_level: Optional[str] = None
    ) -> List[SalaryStatistics]:
        """Fizetési statisztikák lekérése"""
        query = self.db.query(SalaryStatistics)
        
        if job_title:
            query = query.filter(SalaryStatistics.job_title.ilike(f"%{job_title}%"))
        
        if location:
            query = query.filter(SalaryStatistics.location == location)
        
        if experience_level:
            query = query.filter(SalaryStatistics.experience_level == experience_level)
        
        return query.all()
    
    def get_trending_jobs(self, limit: int = 10) -> List[Dict]:
        """Legkeresettebb munkakörök"""
        results = self.db.query(
            Job.title,
            func.count(Job.id).label('count'),
            func.avg(Job.salary_min).label('avg_salary')
        ).filter(
            Job.active == True,
            Job.salary_min.isnot(None)
        ).group_by(
            Job.title
        ).order_by(
            desc('count')
        ).limit(limit).all()
        
        return [
            {
                "title": row.title,
                "count": row.count,
                "avg_salary": round(row.avg_salary) if row.avg_salary else None
            }
            for row in results
        ]
    
    def get_location_statistics(self) -> List[Dict]:
        """Helyszín szerinti statisztikák"""
        results = self.db.query(
            Job.location,
            func.count(Job.id).label('count'),
            func.avg(Job.salary_min).label('avg_salary')
        ).filter(
            Job.active == True,
            Job.location.isnot(None),
            Job.salary_min.isnot(None)
        ).group_by(
            Job.location
        ).order_by(
            desc('count')
        ).all()
        
        return [
            {
                "location": row.location,
                "job_count": row.count,
                "avg_salary": round(row.avg_salary) if row.avg_salary else None
            }
            for row in results
        ]
    
    def get_salary_distribution(self, job_title: Optional[str] = None) -> Dict:
        """Fizetési eloszlás"""
        query = self.db.query(Job).filter(
            Job.active == True,
            Job.salary_min.isnot(None)
        )
        
        if job_title:
            query = query.filter(Job.title.ilike(f"%{job_title}%"))
        
        # Számítások
        avg_salary = query.with_entities(func.avg(Job.salary_min)).scalar()
        min_salary = query.with_entities(func.min(Job.salary_min)).scalar()
        max_salary = query.with_entities(func.max(Job.salary_min)).scalar()
        
        return {
            "avg": round(avg_salary) if avg_salary else None,
            "min": min_salary,
            "max": max_salary,
            "sample_size": query.count()
        }
    
    def calculate_and_store_statistics(self):
        """Statisztikák számítása és tárolása"""
        # Job title szerinti csoportosítás
        job_titles = self.db.query(Job.title).distinct().all()
        
        for (title,) in job_titles:
            jobs = self.db.query(Job).filter(
                Job.title == title,
                Job.active == True,
                Job.salary_min.isnot(None)
            ).all()
            
            if not jobs:
                continue
            
            salaries = [job.salary_min for job in jobs if job.salary_min]
            
            if len(salaries) < 3:  # Minimum 3 adat szükséges
                continue
            
            salaries.sort()
            
            # Statisztikák számítása
            avg_salary = sum(salaries) / len(salaries)
            median_salary = salaries[len(salaries) // 2]
            min_salary = min(salaries)
            max_salary = max(salaries)
            percentile_25 = salaries[len(salaries) // 4]
            percentile_75 = salaries[(3 * len(salaries)) // 4]
            
            # Meglévő statisztika frissítése vagy új létrehozása
            existing = self.db.query(SalaryStatistics).filter(
                SalaryStatistics.job_title == title
            ).first()
            
            if existing:
                existing.avg_salary = avg_salary
                existing.median_salary = median_salary
                existing.min_salary = min_salary
                existing.max_salary = max_salary
                existing.percentile_25 = percentile_25
                existing.percentile_75 = percentile_75
                existing.sample_size = len(salaries)
            else:
                stat = SalaryStatistics(
                    job_title=title,
                    avg_salary=avg_salary,
                    median_salary=median_salary,
                    min_salary=min_salary,
                    max_salary=max_salary,
                    percentile_25=percentile_25,
                    percentile_75=percentile_75,
                    sample_size=len(salaries)
                )
                self.db.add(stat)
        
        self.db.commit()
