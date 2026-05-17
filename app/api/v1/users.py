# 拆分路由，实现用户 CURD，依赖注入数据库
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.exceptions import NotFoundException, ParamException, success_response
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.security import get_password_hash, is_valid_email

from app.core.deps import get_current_user

# 路由分发
router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])

# 创建用户
@router.post('/create', response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
  # 检查用户名是否重复存在
  if db.query(User).filter(User.username == user.username).first():
    raise ParamException('用户已存在')
  if not is_valid_email(user.email):
    raise ParamException('邮箱格式错误')

  # 创建用户
  db_user= User(
    username=user.username,
    email=user.email,
    created_at=user.created_at,
    password=get_password_hash(user.password)
  ) # 转换为数据库模型
  db.add(db_user) # 添加到数据库会话
  db.commit() # 提交事务
  db.refresh(db_user) # 刷新数据库会话中的对象，获取最新数据

  # 返回用户响应，将ORM对象转换为Pydantic模型
  return  success_response(data=UserResponse.model_validate(db_user), message="用户创建成功")


# 删除某个用户
@router.get('/delete/{user_id}', response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # 判断用户是否存在
  db_user = db.query(User).filter(User.id == user_id).first()
  if not db_user:
    raise NotFoundException('用户不存在')

  # 删除用户
  db.delete(db_user)
  db.commit()
  # 返回删除成功响应
  return  success_response(data=None, message="用户删除成功")

# 更新某个用户信息
class UpdateInfo(BaseModel):
  username: str = None
  email: str = None

@router.post('/update/{user_id}', response_model=dict)
def update_user(user_id: int, userInfo: UpdateInfo = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # 判断用户是否存在
  db_user = db.query(User).filter(User.id == user_id).first()
  if not db_user:
    raise NotFoundException('用户不存在')

  # 检查是否有更新信息
  if not userInfo.username and not userInfo.email:
    raise ParamException('参数异常')
  
  if userInfo.email and not is_valid_email(userInfo.email):
    raise ParamException('邮箱格式错误')

  # 更新用户信息
  if userInfo.username:
    db_user.username = userInfo.username
  if userInfo.email:
    db_user.email = userInfo.email

  # 提交事务
  db.commit()
  # 刷新数据库会话中的对象，获取最新数据
  db.refresh(db_user)
  # 返回更新成功响应
  return  success_response(data=None, message="用户更新成功")

# 查询单个用户
@router.get('/{user_id}', response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # 查询用户
  db_user = db.query(User).filter(User.id == user_id).first()
  if not db_user:
    raise NotFoundException('用户不存在')
  return  success_response(data=UserResponse.model_validate(db_user), message="用户查询成功")

# 查询用户列表
@router.get('/all', response_model=dict)
def get_all_users(page: int = 1, page_size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # 查询所有用户
  db_users = db.query(User).offset((page - 1) * page_size).limit(page_size).all()
  # 将ORM对象列表转换为Pydantic模型列表
  user_responses = [UserResponse.model_validate(user) for user in db_users]
  return  success_response(data=user_responses, message="用户列表查询成功")
