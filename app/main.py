from fastapi import FastAPI
from app.core.config import settings
from app.routes import api

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI Agent for 3-Way Invoice Matching"
)

app.include_router(api.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
