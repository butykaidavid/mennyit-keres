"""
Alkalmazás konfigurációs beállítások
Pydantic Settings használatával környezeti változók kezelése
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo
from typing import List, Union
import os
import json


class Settings(BaseSettings):
    """Alkalmazás beállítások"""
    
    # Application
    APP_NAME: str = "Fizetesi_Info_Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-secret-key-in-production"
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api"
    CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:3000", "http://localhost:8000"]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """
        Parse CORS_ORIGINS from various input formats:
        - JSON array string: '["http://localhost:3000","http://localhost:8000"]'
        - Comma-separated string: 'http://localhost:3000,http://localhost:8000'
        - Python list: ["http://localhost:3000", "http://localhost:8000"]
        - Empty string: '' (returns default)
        """
        # If already a list, return it
        if isinstance(v, list):
            return v
        
        # If empty or None, return default
        if not v or v.strip() == "":
            return ["http://localhost:3000", "http://localhost:8000"]
        
        # Try parsing as JSON
        if isinstance(v, str):
            v = v.strip()
            # Check if it looks like JSON
            if v.startswith('[') and v.endswith(']'):
                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return parsed
                except json.JSONDecodeError:
                    pass
            
            # Try comma-separated format
            if ',' in v:
                return [origin.strip() for origin in v.split(',') if origin.strip()]
            
            # Single URL
            return [v]
        
        # Fallback to default
        return ["http://localhost:3000", "http://localhost:8000"]
    
    # Database
    DATABASE_URL: str = "postgresql://admin:password@localhost:5432/fizetesek"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "fizetesek"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    @field_validator('DATABASE_URL', mode='before')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """
        Validate DATABASE_URL is not empty and has proper format.
        If empty or invalid, construct from individual components or use default.
        """
        # If DATABASE_URL is empty or None, return the default
        if not v or (isinstance(v, str) and v.strip() == ""):
            return "postgresql://admin:password@localhost:5432/fizetesek"
        
        # Validate basic URL format
        if isinstance(v, str) and v.strip():
            v = v.strip()
            # Check if it looks like a valid database URL
            if not any(v.startswith(prefix) for prefix in ['postgresql://', 'postgres://', 'sqlite://', 'mysql://']):
                raise ValueError(
                    f"Invalid DATABASE_URL format: '{v}'. "
                    "Expected format: postgresql://user:password@host:port/database"
                )
            return v
        
        # Fallback to default
        return "postgresql://admin:password@localhost:5432/fizetesek"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # JWT Authentication
    JWT_SECRET_KEY: str = "your-jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7
    
    # Scraping
    SCRAPE_INTERVAL: int = 3600
    MAX_PAGES_PER_SITE: int = 10
    REQUEST_DELAY_MIN: int = 1
    REQUEST_DELAY_MAX: int = 3
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Proxy
    USE_PROXY: bool = False
    PROXY_URL: str = ""
    PROXY_USERNAME: str = ""
    PROXY_PASSWORD: str = ""
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_TIMEZONE: str = "Europe/Budapest"
    
    # Monitoring
    SENTRY_DSN: str = ""
    ENABLE_SENTRY: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton settings instance
settings = Settings()
