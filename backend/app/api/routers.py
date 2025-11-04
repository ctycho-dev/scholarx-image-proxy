from fastapi import APIRouter
from app.api.v1 import proxy

api_router = APIRouter()

api_router.include_router(
    proxy.router,
    prefix="/proxy",
    tags=["Proxy"]
)
