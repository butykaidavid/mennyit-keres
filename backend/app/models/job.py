"""
Job model - Állások adatmodellje
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..config.database import Base


class Job(Base):
    """Állás model"""
    
    __tablename__ = "jobs"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Alapadatok
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255))
    location = Column(String(255), index=True)
    
    # Fizetési információk
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String(10), default="HUF")
    salary_period = Column(String(20), default="monthly")  # monthly, hourly, yearly
    
    # Munkakör részletei
    experience_level = Column(String(50))  # junior, medior, senior, lead
    employment_type = Column(String(50))   # full-time, part-time, contract, internship
    skills = Column(JSON)  # Készségek listája
    
    # Leírás és forrás
    description = Column(Text)
    source_url = Column(Text)
    source_portal = Column(String(100))  # profession.hu, jobs.hu, stb.
    
    # Metaadatok
    scraped_at = Column(DateTime, default=datetime.utcnow)
    verified = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    
    # Foreign Keys
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="jobs")
    
    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}')>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "salary_currency": self.salary_currency,
            "salary_period": self.salary_period,
            "experience_level": self.experience_level,
            "employment_type": self.employment_type,
            "skills": self.skills,
            "description": self.description,
            "source_url": self.source_url,
            "source_portal": self.source_portal,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
            "verified": self.verified,
            "active": self.active,
            "category_id": str(self.category_id) if self.category_id else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
