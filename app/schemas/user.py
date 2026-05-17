# 请求校验 + 响应格式化，分离入参和出参
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# 基础用户字段
class UserBase(BaseModel):
  username: str
  created_at: datetime
  email: Optional[EmailStr] = None


# 创建用户（请求参数）
class UserCreate(UserBase):
  password: str

  # 校验密码不超过72字节（bcrypt限制）
  @field_validator('password')
  def validate_password_length(cls, v):
    if len(v.encode('utf-8')) > 72:
      raise ValueError('密码长度不能超过72字节')
    return v


# 用户响应（返回给前端，隐藏密码）
class UserResponse(UserBase):
  id: int

  model_config = {"from_attributes": True}