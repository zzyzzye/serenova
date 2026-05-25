"""文件职责：提供服务健康检查接口，不承担跨模块业务编排。"""

from fastapi import APIRouter

from app.schemas.health import HealthCheckResponse
from app.services.health_service import HealthService

router = APIRouter()


@router.get("", response_model=HealthCheckResponse, summary="健康检查")
async def get_health_status() -> HealthCheckResponse:
    """返回服务当前可用状态。"""
    return await HealthService().get_status()
