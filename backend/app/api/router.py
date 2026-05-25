"""文件职责：聚合所有 API 路由，不承载具体接口实现。"""

from fastapi import APIRouter

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.health import router as health_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(health_router, prefix="/health", tags=["health"])
