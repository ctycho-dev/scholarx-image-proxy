import httpx
from app.services.r2_client import r2_client


def get_r2_client() -> httpx.AsyncClient:
    """Dependency to get R2 client"""
    return r2_client.get_client()
