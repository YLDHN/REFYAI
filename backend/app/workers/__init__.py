# Workers package
from app.workers.tasks import (
    scrape_cadastre,
    scrape_plu,
    scrape_flood_zones,
    scrape_all_project_data,
    analyze_document_with_ai
)

__all__ = [
    "scrape_cadastre",
    "scrape_plu",
    "scrape_flood_zones",
    "scrape_all_project_data",
    "analyze_document_with_ai"
]
