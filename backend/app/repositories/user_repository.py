"""文件职责：提供用户持久化访问边界，负责用户的查询与创建，不处理认证编排。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import UserRecord


class UserRepository:
    """用户仓储。"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> UserRecord | None:
        """按用户名获取用户信息。"""
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        return self._to_record(user)

    async def get_by_email(self, email: str) -> UserRecord | None:
        """按邮箱获取用户信息。"""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        return self._to_record(user)

    async def get_by_user_id(self, user_id: str) -> UserRecord | None:
        """按用户 ID 获取用户信息。"""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        return self._to_record(user)

    async def create_user(
        self,
        *,
        username: str,
        nickname: str,
        email: str,
        password_hash: str,
    ) -> UserRecord:
        """创建新用户并持久化。"""
        user = User(username=username, nickname=nickname, email=email, password_hash=password_hash)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return self._to_record(user)  # type: ignore[return-value]

    def _to_record(self, user: User | None) -> UserRecord | None:
        """将 ORM 对象转换为 schema 记录。"""
        if user is None:
            return None
        return UserRecord(
            user_id=user.id,
            username=user.username,
            nickname=user.nickname,
            email=user.email,
            password_hash=user.password_hash,
            is_active=user.is_active,
        )
