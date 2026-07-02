from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.upload import router as upload_router

app = FastAPI(
    title="Sensitive Data Detection & Compliance Assistant",
    description="AI-powered document analysis and compliance system",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(upload_router)
