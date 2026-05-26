"""文件职责：管理 MySQL 异步 engine 与 session 工厂，不处理任何业务逻辑。"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=False,  # aiomysql 不兼容 pool_pre_ping
    pool_size=10,          # 常驻连接数
    max_overflow=20,       # 允许临时超出的连接数
    pool_timeout=30,       # 获取连接的超时时间（秒）
    pool_recycle=1800,     # 连接回收时间（秒），避免 MySQL 超时断开
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """所有 ORM 模型的基类。"""


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """提供请求级异步数据库会话，用于依赖注入。"""
    async with AsyncSessionLocal() as session:
        yield session
