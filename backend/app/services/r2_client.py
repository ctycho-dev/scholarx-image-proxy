import httpx
from app.core.config import settings


class R2Client:
    def __init__(self):
        self._client: httpx.AsyncClient | None = None
    
    async def start(self):
        """Initialize the httpx client"""
        self._client = httpx.AsyncClient(
            base_url=settings.R2_BASE_URL,
            timeout=30.0,
            limits=httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100
            )
        )
    
    async def stop(self):
        """Close the httpx client"""
        if self._client:
            await self._client.aclose()
    
    def get_client(self) -> httpx.AsyncClient:
        """Get the httpx client instance"""
        if not self._client:
            raise RuntimeError("R2Client not initialized. Call start() first.")
        return self._client


r2_client = R2Client()
