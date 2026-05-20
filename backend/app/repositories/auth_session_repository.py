"""文件职责：负责认证会话在 Redis 中的读写，不处理令牌签发与接口协议。"""

import json
from datetime import UTC, datetime

from redis.asyncio import Redis

from app.core.config import settings


class AuthSessionRepository:
    """认证会话仓储。"""

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def _session_key(self, session_id: str) -> str:
        return f"{settings.redis_key_prefix}:auth:session:{session_id}"

    def _blacklist_key(self, token_id: str) -> str:
        return f"{settings.redis_key_prefix}:auth:blacklist:{token_id}"

    async def save_session(
        self,
        *,
        session_id: str,
        user_id: str,
        username: str,
        refresh_token_id: str,
        expires_at: datetime,
    ) -> None:
        """写入会话信息。"""
        ttl_seconds = max(int((expires_at - datetime.now(UTC)).total_seconds()), 1)
        payload = {
            "session_id": session_id,
            "user_id": user_id,
            "username": username,
            "refresh_token_id": refresh_token_id,
            "expires_at": expires_at.isoformat(),
        }
        await self.redis_client.set(
            self._session_key(session_id),
            json.dumps(payload),
            ex=ttl_seconds,
        )

    async def get_session(self, session_id: str) -> dict | None:
        """读取会话信息。"""
        raw_value = await self.redis_client.get(self._session_key(session_id))
        if raw_value is None:
            return None
        return json.loads(raw_value)

    async def revoke_session(self, session_id: str) -> None:
        """删除指定会话。"""
        await self.redis_client.delete(self._session_key(session_id))

    async def blacklist_token(self, token_id: str, expires_at: datetime) -> None:
        """加入访问令牌黑名单。"""
        ttl_seconds = max(int((expires_at - datetime.now(UTC)).total_seconds()), 1)
        await self.redis_client.set(self._blacklist_key(token_id), "1", ex=ttl_seconds)

    async def is_token_blacklisted(self, token_id: str) -> bool:
        """判断访问令牌是否已被撤销。"""
        return await self.redis_client.exists(self._blacklist_key(token_id)) > 0

