"""文件职责：管理 Redis 异步客户端的创建与关闭，不处理业务级会话规则。"""

from redis.asyncio import Redis, from_url

from app.core.config import settings

_redis_client: Redis | None = None


async def get_redis_client() -> Redis:
    """获取复用的 Redis 异步客户端。"""
    global _redis_client
    if _redis_client is None:
        _redis_client = from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
        await _redis_client.ping()
    return _redis_client


async def close_redis_client() -> None:
    """关闭 Redis 异步客户端连接。"""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None
