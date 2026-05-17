# app/utils/security.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings
import re

# 🔥 替换为：无长度限制、永不报错的加密算法（完美适配入门）
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 加密：无需任何截断，支持任意长度密码
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 校验：和加密逻辑完全匹配
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 正则校验邮箱格式
def is_valid_email(email: str) -> bool:
    return re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None

# 生成JWT令牌
def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    # 自定义过期时间
    expire = datetime.now() + expires_delta
  else:
    # 默认过期时间
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)