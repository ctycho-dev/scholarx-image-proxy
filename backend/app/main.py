from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import get_logger
from app.api.routers import api_router
from app.services.r2_client import r2_client
from app.middleware.logging import RequestLoggingMiddleware

logger = get_logger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """FastAPI application lifecycle."""

    await r2_client.start()
    logger.info("Starting up the ScholarX Image Proxy API...")

    yield

    await r2_client.stop()
    logger.info("Shutting down the ScholarX Image Proxy API...")


app = FastAPI(
    title="ScholarX Image Proxy",
    description="Proxy server for Cloudflare R2 images to bypass Russian throttling",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(RequestLoggingMiddleware)

app.include_router(api_router, prefix=settings.API_VERSION)


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {
        "message": "ScholarX Image Proxy API",
        "health": "/health",
        "target": settings.R2_BASE_URL,
        "usage": "GET /<path-to-image>"
    }
