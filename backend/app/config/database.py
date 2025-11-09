"""
Database configuration
SQLAlchemy setup és session kezelés
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings
import sys
import logging

logger = logging.getLogger(__name__)

# Validate DATABASE_URL before creating engine
if not settings.DATABASE_URL or settings.DATABASE_URL.strip() == "":
    error_msg = (
        "DATABASE_URL is empty or not set!\n"
        "Please set the DATABASE_URL environment variable.\n"
        "Example: DATABASE_URL=postgresql://user:password@host:port/database\n"
        f"Current value: '{settings.DATABASE_URL}'"
    )
    logger.error(error_msg)
    raise ValueError(error_msg)

try:
    # Database engine
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=settings.DEBUG
    )
    logger.info(f"Database engine created successfully")
except Exception as e:
    error_msg = (
        f"Failed to create database engine!\n"
        f"DATABASE_URL: {settings.DATABASE_URL}\n"
        f"Error: {str(e)}\n"
        "Please check your DATABASE_URL format and ensure the database is accessible."
    )
    logger.error(error_msg)
    raise ValueError(error_msg) from e

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency for FastAPI
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
