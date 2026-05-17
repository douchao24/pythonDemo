from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.config import settings
from app.core.exceptions import AuthFailException, success_response
from app.models.user import User
from app.utils.security import verify_password, create_access_token


router = APIRouter(prefix="/api/v1//auth", tags=["登录认证"])


# 接口登录，获取token
@router.post('/login')
def login(
  response: Response,
  form_data: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(get_db)
):
  # 根据用户名查用户
  user=db.query(User).filter(User.username == form_data.username).first()
  if not user:
    raise AuthFailException()

  # 校验密码
  if not verify_password(form_data.password, user.password):
    raise AuthFailException()

  # 生成token JWT令牌
  access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={"sub": user.username},
    expires_delta=access_token_expires
  )

  # 把token写进cookie
  response.set_cookie(
     key="access_token",                # cookie 名称（固定）
    value=f"Bearer {access_token}",    # 值
    httponly=True,                     # 禁止 JS 获取，防 XSS
    max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 过期时间
    samesite="lax",                    # 安全策略
    secure=False     
  )

  return success_response(
    data={"token_type": "bearer"},
    message="登录成功"
  )


