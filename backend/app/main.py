from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.users import router as users_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(
    health_router,
    prefix=settings.API_V1_STR,
    tags=["Health"],
)

app.include_router(
    users_router,
    prefix=settings.API_V1_STR,
)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}"
    }