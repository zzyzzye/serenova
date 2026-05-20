"""文件职责：提供认证依赖注入与当前用户解析，不处理登录业务编排。"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth import AccessTokenContext
from app.services.auth_service import AuthService

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AccessTokenContext:
    """解析并校验当前请求中的访问令牌。"""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少访问令牌。",
        )
    return await AuthService().authenticate_access_token(credentials.credentials)

