"""
Configuration Celery pour tâches asynchrones
"""
from celery import Celery
from app.core.config import settings

# Créer l'application Celery
celery_app = Celery(
    "refyai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Paris",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes max
    task_soft_time_limit=25 * 60,  # Soft limit à 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Import des tâches
celery_app.autodiscover_tasks(["app.workers"])
