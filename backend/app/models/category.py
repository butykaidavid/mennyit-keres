"""
Category model - Kategória adatmodellje
"""

from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..config.database import Base


class Category(Base):
    """Kategória model"""
    
    __tablename__ = "categories"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Alapadatok
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Hierarchia támogatás (szülő kategória)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    jobs = relationship("Job", back_populates="category")
    children = relationship("Category", backref="parent", remote_side=[id])
    
    def __repr__(self):
        return f"<Category(name='{self.name}', slug='{self.slug}')>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
