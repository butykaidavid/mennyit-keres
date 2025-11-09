"""
Salary Statistics model - Fizetési statisztikák adatmodellje
"""

from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..config.database import Base


class SalaryStatistics(Base):
    """Fizetési statisztikák model"""
    
    __tablename__ = "salary_statistics"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Munkakör információk
    job_title = Column(String(255), nullable=False, index=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    
    # Statisztikai adatok
    avg_salary = Column(Float)          # Átlag fizetés
    median_salary = Column(Float)       # Medián fizetés
    min_salary = Column(Float)          # Minimum fizetés
    max_salary = Column(Float)          # Maximum fizetés
    percentile_25 = Column(Float)       # 25. percentilis
    percentile_75 = Column(Float)       # 75. percentilis
    
    # Minta mérete
    sample_size = Column(Integer)       # Hány álláshirdetés alapján
    
    # Szűrők
    location = Column(String(255))      # Helyszín (opcionális)
    experience_level = Column(String(50))  # Tapasztalati szint (opcionális)
    
    # Timestamps
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship("Category")
    
    def __repr__(self):
        return f"<SalaryStatistics(job_title='{self.job_title}', avg={self.avg_salary})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "job_title": self.job_title,
            "category_id": str(self.category_id) if self.category_id else None,
            "avg_salary": self.avg_salary,
            "median_salary": self.median_salary,
            "min_salary": self.min_salary,
            "max_salary": self.max_salary,
            "percentile_25": self.percentile_25,
            "percentile_75": self.percentile_75,
            "sample_size": self.sample_size,
            "location": self.location,
            "experience_level": self.experience_level,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
