#用户表结构（ORM）
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base # 导入数据库基类

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String(50), unique=True, index=True, comment="用户名")
  password = Column(String(100), comment="密码")
  email = Column(String(100), unique=True, index=True, comment="邮箱")
  created_at = Column(DateTime, default=DateTime, comment="创建时间")
