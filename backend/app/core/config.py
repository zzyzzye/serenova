"""文件职责：定义应用配置来源与默认值，不处理运行时业务逻辑。"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "video-backend"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    jwt_secret_key: str = "please-change-this-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    redis_url: str = "redis://localhost:6379/0"
    redis_key_prefix: str = "video"
    demo_username: str = "admin"
    demo_password: str = "admin123456"
    demo_user_id: str = "demo-admin"
    demo_nickname: str = "演示管理员"
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )


@lru_cache
def get_settings() -> Settings:
    """缓存配置实例，避免重复解析环境变量。"""
    return Settings()


settings = get_settings()
