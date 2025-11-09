"""
Alkalmazás konfigurációs beállítások
Pydantic Settings használatával környezeti változók kezelése
"""

from pydantic_settings import BaseSettings
from typing import List
import os


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
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database
    DATABASE_URL: str = "postgresql://admin:password@localhost:5432/fizetesek"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "fizetesek"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
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
