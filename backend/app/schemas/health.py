"""文件职责：定义健康检查接口的响应结构，不处理状态探测流程。"""

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """健康检查响应。"""

    status: str
    service: str
    version: str
