"""文件职责：提供登录、刷新、退出和当前用户查询接口，不承载认证编排细节。"""

from fastapi import APIRouter, Depends

from app.api.deps.auth import get_current_access_token
from app.schemas.auth import (
    AccessTokenContext,
    LoginRequest,
    LogoutResponse,
    RefreshTokenRequest,
    TokenPairResponse,
    UserProfile,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenPairResponse, summary="账号登录")
async def login(payload: LoginRequest) -> TokenPairResponse:
    """校验账号密码并返回令牌对。"""
    return await AuthService().login(payload)


@router.post("/refresh", response_model=TokenPairResponse, summary="刷新令牌")
async def refresh_token(payload: RefreshTokenRequest) -> TokenPairResponse:
    """基于刷新令牌签发新的访问令牌与刷新令牌。"""
    return await AuthService().refresh_token(payload.refresh_token)


@router.post("/logout", response_model=LogoutResponse, summary="退出登录")
async def logout(
    token_context: AccessTokenContext = Depends(get_current_access_token),
) -> LogoutResponse:
    """撤销当前会话并使访问令牌失效。"""
    await AuthService().logout(token_context)
    return LogoutResponse(message="已退出登录。")


@router.get("/me", response_model=UserProfile, summary="当前用户")
async def get_current_user(
    token_context: AccessTokenContext = Depends(get_current_access_token),
) -> UserProfile:
    """返回当前访问令牌对应的用户信息。"""
    return token_context.user
