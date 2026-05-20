"""文件职责：编排账号登录、令牌刷新、会话撤销与当前用户解析，不负责 HTTP 协议细节。"""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import create_token, decode_token, verify_password
from app.core.security import TokenDecodeError
from app.db.redis import get_redis_client
from app.repositories.auth_session_repository import AuthSessionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AccessTokenContext, LoginRequest, TokenPairResponse, UserProfile


class AuthService:
    """认证服务。"""

    def __init__(self):
        self.user_repository = UserRepository()

    async def login(self, payload: LoginRequest) -> TokenPairResponse:
        """校验账号密码并创建登录会话。"""
        user = await self.user_repository.get_by_username(payload.username)
        if user is None or not user.is_active:
            raise self._invalid_credentials_error()
        if not verify_password(payload.password, user.password_hash):
            raise self._invalid_credentials_error()
        return await self._issue_token_pair(
            user=UserProfile.model_validate(user.model_dump()),
        )

    async def refresh_token(self, refresh_token: str) -> TokenPairResponse:
        """刷新令牌并轮换会话信息。"""
        payload = self._decode_and_validate_token(refresh_token, expected_type="refresh")
        session_repository = await self._get_session_repository()
        session = await session_repository.get_session(payload["sid"])
        if session is None:
            raise self._unauthorized_error("登录会话已失效，请重新登录。")
        if session["refresh_token_id"] != payload["jti"]:
            raise self._unauthorized_error("刷新令牌已失效，请重新登录。")

        user = await self.user_repository.get_by_user_id(payload["sub"])
        if user is None or not user.is_active:
            raise self._unauthorized_error("用户状态不可用，请重新登录。")

        await session_repository.revoke_session(payload["sid"])
        return await self._issue_token_pair(
            user=UserProfile.model_validate(user.model_dump()),
        )

    async def authenticate_access_token(self, access_token: str) -> AccessTokenContext:
        """校验访问令牌并返回当前用户上下文。"""
        payload = self._decode_and_validate_token(access_token, expected_type="access")
        session_repository = await self._get_session_repository()
        if await session_repository.is_token_blacklisted(payload["jti"]):
            raise self._unauthorized_error("访问令牌已失效，请重新登录。")
        session = await session_repository.get_session(payload["sid"])
        if session is None:
            raise self._unauthorized_error("登录会话已失效，请重新登录。")

        user = await self.user_repository.get_by_user_id(payload["sub"])
        if user is None or not user.is_active:
            raise self._unauthorized_error("用户状态不可用，请重新登录。")

        return AccessTokenContext(
            token_id=payload["jti"],
            session_id=payload["sid"],
            user=UserProfile.model_validate(user.model_dump()),
            expires_at=datetime.fromtimestamp(payload["exp"], tz=UTC),
        )

    async def logout(self, token_context: AccessTokenContext) -> None:
        """撤销当前会话并拉黑当前访问令牌。"""
        session_repository = await self._get_session_repository()
        await session_repository.revoke_session(token_context.session_id)
        await session_repository.blacklist_token(
            token_context.token_id,
            token_context.expires_at,
        )

    async def _issue_token_pair(self, *, user: UserProfile) -> TokenPairResponse:
        """创建访问令牌、刷新令牌和 Redis 会话。"""
        session_id = uuid4().hex
        access_token, _, access_expires_at = create_token(
            subject=user.user_id,
            token_type="access",
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
            session_id=session_id,
            username=user.username,
        )
        refresh_token, refresh_token_id, refresh_expires_at = create_token(
            subject=user.user_id,
            token_type="refresh",
            expires_delta=timedelta(days=settings.refresh_token_expire_days),
            session_id=session_id,
            username=user.username,
        )
        session_repository = await self._get_session_repository()
        await session_repository.save_session(
            session_id=session_id,
            user_id=user.user_id,
            username=user.username,
            refresh_token_id=refresh_token_id,
            expires_at=refresh_expires_at,
        )
        return TokenPairResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_at=access_expires_at,
            refresh_token_expires_at=refresh_expires_at,
            user=user,
        )

    async def _get_session_repository(self) -> AuthSessionRepository:
        """构建 Redis 会话仓储。"""
        redis_client = await get_redis_client()
        return AuthSessionRepository(redis_client)

    def _decode_and_validate_token(self, token: str, *, expected_type: str) -> dict:
        """解析 JWT 并校验类型字段。"""
        try:
            payload = decode_token(token)
        except TokenDecodeError as exc:
            raise self._unauthorized_error("令牌无效或已过期。") from exc
        if payload.get("type") != expected_type:
            raise self._unauthorized_error("令牌类型不匹配。")
        return payload

    def _invalid_credentials_error(self) -> HTTPException:
        """返回统一的账号密码错误。"""
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误。",
        )

    def _unauthorized_error(self, detail: str) -> HTTPException:
        """返回统一的鉴权失败异常。"""
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )
