"""文件职责：聚合所有 API 版本路由，不承载具体接口实现。"""

from fastapi import APIRouter

from app.api.v1.router import router as v1_router

api_router = APIRouter()
api_router.include_router(v1_router, prefix="/v1")
