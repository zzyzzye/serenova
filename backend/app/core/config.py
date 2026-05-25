"""定义应用配置来源与默认值，不处理运行时业务逻辑。"""

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
    database_url: str = "mysql+aiomysql://root:root@localhost:3306/serenova"
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    smtp_from: str = ""
    smtp_use_tls: bool = True
    reset_token_expire_minutes: int = 30
    frontend_url: str = "http://localhost:5173"


@lru_cache
def get_settings() -> Settings:
    """缓存配置实例，避免重复解析环境变量。"""
    return Settings()


settings = get_settings()
