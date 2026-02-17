from fastapi import APIRouter
from app.routes import match_routes

router = APIRouter()

router.include_router(match_routes.router, prefix="/match", tags=["matching"])
