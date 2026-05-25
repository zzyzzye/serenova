"""文件职责：定义认证链路输入输出结构，不承载登录校验与令牌处理过程。"""

from datetime import datetime

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    """注册请求。"""

    username: str = Field(min_length=3, max_length=64)
    nickname: str = Field(min_length=1, max_length=64)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    """登录请求。"""

    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求。"""

    refresh_token: str = Field(min_length=20)


class ForgotPasswordRequest(BaseModel):
    """忘记密码请求。"""

    email: str = Field(min_length=5, max_length=255)


class ResetPasswordRequest(BaseModel):
    """重置密码请求。"""

    token: str = Field(min_length=1)
    new_password: str = Field(min_length=6, max_length=128)


class UserProfile(BaseModel):
    """对外返回的用户信息。"""

    user_id: str
    username: str
    nickname: str


class UserRecord(UserProfile):
    """仓储层使用的用户记录。"""

    email: str | None = None
    password_hash: str
    is_active: bool = True


class TokenPairResponse(BaseModel):
    """登录或刷新成功后的令牌响应。"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    access_token_expires_at: datetime
    refresh_token_expires_at: datetime
    user: UserProfile


class AccessTokenContext(BaseModel):
    """访问令牌解析后的上下文。"""

    token_id: str
    session_id: str
    user: UserProfile
    expires_at: datetime


class LogoutResponse(BaseModel):
    """退出登录响应。"""

    message: str
