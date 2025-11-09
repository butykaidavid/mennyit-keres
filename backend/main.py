"""
Magyar Fizetési Információs Platform - Backend API
FastAPI alkalmazás az állások és fizetési információk kezelésére
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.config.settings import settings
from app.routers import jobs, categories, statistics, admin

# Logging beállítás
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app inicializálás
app = FastAPI(
    title="Fizetési Info Platform API",
    description="API a magyar munkaerőpiaci fizetési információk kezeléséhez",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Belső szerverhiba történt"}
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """API health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.APP_ENV
    }


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Fizetési Info Platform API",
        "docs": "/docs",
        "health": "/health"
    }


# Routers
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["statistics"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Application starting up...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Database kapcsolat ellenőrzése
    # await check_database_connection()


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 Application shutting down...")
    # Cleanup tasks


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
