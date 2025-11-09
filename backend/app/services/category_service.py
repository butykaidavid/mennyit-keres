"""
Category Service
Kategóriákkal kapcsolatos business logic
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..models.category import Category
from ..models.job import Job


class CategoryService:
    """Category service osztály"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_categories(self) -> List[Category]:
        """Összes kategória"""
        return self.db.query(Category).order_by(Category.name).all()
    
    def get_category_by_slug(self, slug: str) -> Optional[Category]:
        """Kategória lekérése slug alapján"""
        return self.db.query(Category).filter(Category.slug == slug).first()
    
    def get_category_by_id(self, category_id: UUID) -> Optional[Category]:
        """Kategória lekérése ID alapján"""
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def get_jobs_for_category(self, category_id: UUID, skip: int = 0, limit: int = 10) -> List[Job]:
        """Kategóriához tartozó állások"""
        return self.db.query(Job).filter(
            Job.category_id == category_id,
            Job.active == True
        ).offset(skip).limit(limit).all()
    
    def get_job_count_for_category(self, category_id: UUID) -> int:
        """Kategóriához tartozó állások száma"""
        return self.db.query(Job).filter(
            Job.category_id == category_id,
            Job.active == True
        ).count()
    
    def create_category(self, name: str, slug: str, description: str = None) -> Category:
        """Új kategória létrehozása"""
        category = Category(name=name, slug=slug, description=description)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
