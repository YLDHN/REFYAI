from fastapi import APIRouter

# Import des routers
from app.api import (
    auth,
    projects,
    documents,
    financial,
    excel,
    chat,
    questionnaire,
    showstoppers,
    market,
    interest_rate,
    capex,
    admin_delays,
    timeline,
    asset_management,
    scraper,
    compliance,
    scoring,
    exports
)

api_router = APIRouter(prefix="/api")

# Inclusion des routes
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(documents.router)
api_router.include_router(financial.router)
api_router.include_router(excel.router)
api_router.include_router(chat.router)
api_router.include_router(questionnaire.router)
api_router.include_router(showstoppers.router)
api_router.include_router(market.router)
api_router.include_router(interest_rate.router)
api_router.include_router(capex.router)
api_router.include_router(admin_delays.router)
api_router.include_router(timeline.router)
api_router.include_router(asset_management.router)
api_router.include_router(scraper.router)
api_router.include_router(compliance.router)
api_router.include_router(scoring.router)
api_router.include_router(exports.router)
