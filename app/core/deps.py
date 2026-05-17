from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

# auto_error=False：让 OAuth2 不主动抛 401，给我们 Cookie 读取的机会
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # 1. 优先从 Cookie 读取 Token
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        # 去掉 Bearer 前缀
        if cookie_token.startswith("Bearer "):
            cookie_token = cookie_token[7:]
        final_token = cookie_token
    else:
        # 2. Cookie 里没有，再用 Header 里的 Token
        final_token = token

    # 3. 没找到 Token，直接抛 401
    if not final_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # 4. 校验 Token
    try:
        payload = jwt.decode(
            final_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="token无效")
    except JWTError:
        raise HTTPException(status_code=401, detail="token无效或已过期")

    # 5. 查用户
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")

    return user