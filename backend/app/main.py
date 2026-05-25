"""装配 FastAPI 应用实例、中间件、生命周期与顶层路由，不处理具体业务细节。"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.mysql import Base, engine
from app.db.redis import close_redis_client, get_redis_client
import app.models.user  # noqa: F401  确保 ORM 模型注册到 Base.metadata


@asynccontextmanager
async def lifespan(_: FastAPI):
    """管理应用启动与关闭时的基础设施资源。"""
    # 全新安装时自动建表（已有表不会重复创建）
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await get_redis_client()
    yield
    await close_redis_client()
    await engine.dispose()


def create_application() -> FastAPI:
    """创建并配置 FastAPI 应用实例。"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.api_prefix)
    return app


app = create_application()
