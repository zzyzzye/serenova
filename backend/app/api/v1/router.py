"""文件职责：组织 V1 版本下的端点路由，不负责业务规则计算。"""

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(health_router, prefix="/health", tags=["health"])
