from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.monitoring import MonitoringMiddleware, setup_logging
import os

# Setup logging
os.makedirs("logs", exist_ok=True)
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API Backend pour REFY AI - Analyse de faisabilité immobilière"
)

# Monitoring middleware
app.add_middleware(MonitoringMiddleware)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import time
from datetime import datetime

# Variables pour les métriques
start_time = time.time()
request_count = 0
failed_requests = 0
total_response_time = 0

@app.get("/")
async def root():
    return {
        "message": "REFY AI API",
        "version": settings.VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    uptime = time.time() - start_time
    success_rate = 100 if request_count == 0 else ((request_count - failed_requests) / request_count) * 100
    avg_response = total_response_time / request_count if request_count > 0 else 0
    
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": time.time(),
        "metrics": {
            "uptime_seconds": round(uptime, 2),
            "total_requests": request_count,
            "failed_requests": failed_requests,
            "success_rate": round(success_rate, 2),
            "avg_response_time_ms": round(avg_response * 1000, 2)
        }
    }

# Import des routes
from app.api import api_router
app.include_router(api_router)
