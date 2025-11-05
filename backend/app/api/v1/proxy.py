from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
from app.core.config import settings
from app.core.logger import get_logger
from app.core.dependencies import get_r2_client
from app.core.decorators import handle_httpx_errors


logger = get_logger()

router = APIRouter()


@router.get("/{path:path}")
@handle_httpx_errors
async def proxy_image(
    path: str,
    client: httpx.AsyncClient = Depends(get_r2_client)
):
    """
    Proxy images from Cloudflare R2.
    Nginx caches responses, so this only runs on cache MISS.
    """
    if not path:
        return JSONResponse(
            status_code=400,
            content={"error": "Path is required"}
        )

    url = f"/{path}"
    r2_response = await client.get(url, follow_redirects=True)

    response_headers = {
        "Content-Type": r2_response.headers.get(
            "content-type",
            "application/octet-stream"
        ),
        # Browser & CDN cache for 1 year, immutable = never revalidate
        "Cache-Control": "public, max-age=31536000, immutable",
        # Cloudflare-specific: overrides Cache-Control for Cloudflare edge
        "CDN-Cache-Control": "max-age=31536000",
        # Tell browser/CDN this can vary based on Accept header (WebP vs JPEG)
        "Vary": "Accept",
    }

    if "content-length" in r2_response.headers:
        response_headers["Content-Length"] = r2_response.headers["content-length"]

    return StreamingResponse(
        content=r2_response.iter_bytes(chunk_size=8192),
        status_code=r2_response.status_code,
        headers=response_headers,
        media_type=r2_response.headers.get("content-type")
    )
