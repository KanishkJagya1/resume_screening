# api/main.py
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from typing import List, Optional, Dict, Any
import logging
import os
from datetime import datetime
import uuid

# Import your existing modules
from api.routes import resume_router, sentiment_router, health_router
from api.middleware import RateLimitMiddleware, LoggingMiddleware
from api.models import APIResponse, ErrorResponse
from config.settings import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="HR AI Toolkit API",
    description="AI-powered HR automation for resume screening and sentiment analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Get settings
settings = get_settings()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)

# Security
security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple API key authentication"""
    if not credentials:
        return None
    
    if credentials.credentials != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return {"api_key": credentials.credentials}

# Include routers
app.include_router(health_router.router, prefix="/api/v1", tags=["health"])
app.include_router(
    resume_router.router, 
    prefix="/api/v1/resume", 
    tags=["resume-screening"],
    dependencies=[Depends(get_current_user)] if settings.REQUIRE_AUTH else []
)
app.include_router(
    sentiment_router.router, 
    prefix="/api/v1/sentiment", 
    tags=["sentiment-analysis"],
    dependencies=[Depends(get_current_user)] if settings.REQUIRE_AUTH else []
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting HR AI Toolkit API...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down HR AI Toolkit API...")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=True,
            message=exc.detail,
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=True,
            message="Internal server error",
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )

@app.get("/", response_model=APIResponse)
async def root():
    """Root endpoint"""
    return APIResponse(
        success=True,
        message="HR AI Toolkit API is running",
        data={"version": "1.0.0", "status": "healthy"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4
    )