"""文件职责：提供用户身份查询边界，当前仅承接演示账号，不处理认证编排。"""

from app.core.config import settings
from app.core.security import hash_password
from app.schemas.auth import UserRecord


class UserRepository:
    """用户仓储。"""

    def __init__(self):
        self.demo_password_hash = hash_password(settings.demo_password)

    async def get_by_username(self, username: str) -> UserRecord | None:
        """按用户名获取用户信息。"""
        if username != settings.demo_username:
            return None
        return UserRecord(
            user_id=settings.demo_user_id,
            username=settings.demo_username,
            nickname=settings.demo_nickname,
            password_hash=self.demo_password_hash,
            is_active=True,
        )

    async def get_by_user_id(self, user_id: str) -> UserRecord | None:
        """按用户 ID 获取用户信息。"""
        if user_id != settings.demo_user_id:
            return None
        return UserRecord(
            user_id=settings.demo_user_id,
            username=settings.demo_username,
            nickname=settings.demo_nickname,
            password_hash=self.demo_password_hash,
            is_active=True,
        )
