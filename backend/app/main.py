from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import settings
from app.core.monitoring import MonitoringMiddleware, setup_logging
import os
import time
import asyncio
from typing import Callable

# Setup logging
os.makedirs("logs", exist_ok=True)
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API Backend pour REFY AI - Analyse de faisabilité immobilière",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Redirection /docs vers /api/docs pour compatibilité
@app.get("/docs", include_in_schema=False)
async def redirect_docs():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/docs")

# Middleware de timeout global
@app.middleware("http")
async def timeout_middleware(request: Request, call_next: Callable):
    try:
        # Timeout de 60s pour toutes les requêtes
        return await asyncio.wait_for(
            call_next(request),
            timeout=60.0
        )
    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={"detail": "La requête a pris trop de temps"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Erreur serveur: {str(e)}"},
        )

# Monitoring middleware
app.add_middleware(MonitoringMiddleware)

# Configuration CORS améliorée
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight 1h
)

# Gestion globale des erreurs de validation
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Erreur de validation",
            "errors": exc.errors(),
        },
    )

# Gestion globale des erreurs HTTP
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Gestion globale des erreurs non gérées
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    import traceback
    error_trace = traceback.format_exc()
    print(f"Erreur non gérée: {error_trace}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Une erreur interne est survenue",
            "error": str(exc) if settings.DEBUG else None,
        },
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
        "status": "running",
        "docs": "/api/docs",
    }

@app.get("/health")
async def health_check():
    """Endpoint de health check avec métriques."""
    uptime = time.time() - start_time
    success_rate = 100 if request_count == 0 else ((request_count - failed_requests) / request_count) * 100
    avg_response = total_response_time / request_count if request_count > 0 else 0
    
    # Test de connexion DB
    db_status = "healthy"
    try:
        from app.core.database import engine
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "version": settings.VERSION,
        "timestamp": time.time(),
        "database": db_status,
        "metrics": {
            "uptime_seconds": round(uptime, 2),
            "total_requests": request_count,
            "failed_requests": failed_requests,
            "success_rate": round(success_rate, 2),
            "avg_response_time_ms": round(avg_response * 1000, 2)
        }
    }

@app.get("/api/status")
async def api_status():
    """Status rapide pour les tests de connectivité."""
    return {
        "ok": True,
        "version": settings.VERSION,
        "timestamp": time.time(),
    }

# Import des routes
from app.api import api_router
app.include_router(api_router)
