# 统一管理配置，自动读取 .env
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
  # 服务器基础配置
  APP_NAME: str
  APP_VERSION: str
  DEBUG: bool = False

  # 数据库配置
  DATABASE_URL: str

  # JWT配置
  SECRET_KEY: str
  ALGORITHM: str
  ACCESS_TOKEN_EXPIRE_MINUTES: int

  # 读取.env配置
  model_config= SettingsConfigDict(env_file=".env")


# 全局单例配置
settings = Settings()