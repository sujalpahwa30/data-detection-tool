from fastapi import APIRouter

router = APIRouter(
    tags=["Health"]
)


@router.get("/")
async def root():
    return {
        "message": "Sensitive Data Detection & Compliance Assistant API",
        "status": "running",
    }


@router.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }