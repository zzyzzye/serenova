"""文件职责：封装密码散列与 JWT 签发校验能力，不处理认证流程编排。"""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings

password_hasher = PasswordHash.recommended()


class TokenDecodeError(Exception):
    """令牌解码失败。"""


def hash_password(password: str) -> str:
    """生成密码散列。"""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """校验明文密码与散列是否匹配。"""
    return password_hasher.verify(password, password_hash)


def create_token(
    *,
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    session_id: str,
    username: str,
) -> tuple[str, str, datetime]:
    """创建指定类型的 JWT。"""
    now = datetime.now(UTC)
    expires_at = now + expires_delta
    token_id = uuid4().hex
    payload = {
        "sub": subject,
        "type": token_type,
        "sid": session_id,
        "jti": token_id,
        "username": username,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return token, token_id, expires_at


def decode_token(token: str) -> dict:
    """解码并校验 JWT。"""
    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except (ExpiredSignatureError, InvalidTokenError) as exc:
        raise TokenDecodeError(str(exc)) from exc

