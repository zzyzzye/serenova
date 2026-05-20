"""文件职责：编排健康检查返回内容，不负责 HTTP 协议细节与持久化访问。"""

from app.core.config import settings
from app.schemas.health import HealthCheckResponse


class HealthService:
    """健康检查服务。"""

    async def get_status(self) -> HealthCheckResponse:
        """构建健康检查响应。"""
        return HealthCheckResponse(
            status="ok",
            service=settings.app_name,
            version=settings.app_version,
        )
