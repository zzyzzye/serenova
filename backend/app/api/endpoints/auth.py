"""文件职责：提供注册、登录、刷新、退出、密码重置和当前用户查询接口，不承载认证编排细节。"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth import get_current_access_token
from app.db.mysql import get_db_session
from app.schemas.auth import (
    AccessTokenContext,
    ForgotPasswordRequest,
    LoginRequest,
    LogoutResponse,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenPairResponse,
    UserProfile,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=TokenPairResponse, status_code=201, summary="账号注册")
async def register(
    payload: RegisterRequest,
    session: AsyncSession = Depends(get_db_session),
) -> TokenPairResponse:
    """注册新账号并返回令牌对。"""
    return await AuthService(session).register(payload)


@router.post("/login", response_model=TokenPairResponse, summary="账号登录")
async def login(
    payload: LoginRequest,
    session: AsyncSession = Depends(get_db_session),
) -> TokenPairResponse:
    """校验账号密码并返回令牌对。"""
    return await AuthService(session).login(payload)


@router.post("/refresh", response_model=TokenPairResponse, summary="刷新令牌")
async def refresh_token(
    payload: RefreshTokenRequest,
    session: AsyncSession = Depends(get_db_session),
) -> TokenPairResponse:
    """基于刷新令牌签发新的访问令牌与刷新令牌。"""
    return await AuthService(session).refresh_token(payload.refresh_token)


@router.post("/logout", response_model=LogoutResponse, summary="退出登录")
async def logout(
    token_context: AccessTokenContext = Depends(get_current_access_token),
    session: AsyncSession = Depends(get_db_session),
) -> LogoutResponse:
    """撤销当前会话并使访问令牌失效。"""
    await AuthService(session).logout(token_context)
    return LogoutResponse(message="已退出登录。")


@router.get("/me", response_model=UserProfile, summary="当前用户")
async def get_current_user(
    token_context: AccessTokenContext = Depends(get_current_access_token),
) -> UserProfile:
    """返回当前访问令牌对应的用户信息。"""
    return token_context.user


@router.post("/forgot-password", status_code=200, summary="忘记密码")
async def forgot_password(
    payload: ForgotPasswordRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """发送密码重置邮件。"""
    await AuthService(session).forgot_password(payload)
    return {"message": "如果该邮箱已注册，重置链接已发送。"}


@router.post("/reset-password", status_code=200, summary="重置密码")
async def reset_password(
    payload: ResetPasswordRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """通过重置 token 更新密码。"""
    await AuthService(session).reset_password(payload)
    return {"message": "密码已重置，请使用新密码登录。"}
