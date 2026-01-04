"""
Middleware de monitoring et logging pour l'API
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import logging
from datetime import datetime

logger = logging.getLogger("refyai")

class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Début de la requête
        start_time = time.time()
        request_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{id(request)}"
        
        # Log requête entrante
        logger.info(f"[{request_id}] {request.method} {request.url.path}")
        
        # Exécuter la requête
        try:
            response = await call_next(request)
            
            # Temps de traitement
            process_time = time.time() - start_time
            
            # Log réponse
            logger.info(
                f"[{request_id}] {request.method} {request.url.path} "
                f"- Status: {response.status_code} "
                f"- Time: {process_time:.3f}s"
            )
            
            # Ajouter headers custom
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"[{request_id}] {request.method} {request.url.path} "
                f"- ERROR: {str(e)} "
                f"- Time: {process_time:.3f}s"
            )
            raise

# Configuration du logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/refyai.log'),
            logging.StreamHandler()
        ]
    )
