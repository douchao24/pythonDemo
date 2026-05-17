# 数据库连接
from sqlalchemy import create_engine # 创建数据库引擎
from sqlalchemy.ext.declarative import declarative_base # 声明式基类
from sqlalchemy.orm import sessionmaker # 会话工厂类
from app.core.config import settings # 导入配置

# 创建数据库引擎
engine = create_engine(
  settings.DATABASE_URL,
  connect_args={"check_same_thread": False} # 禁用线程安全检查
)

# 数据库会话类
# 用于创建数据库会话实例，每个请求创建一个会话，请求结束后关闭会话。
# 会话工厂类，用于创建数据库会话实例。
# 会话实例用于执行数据库操作，如查询、添加、删除等。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 会话工厂类

# ORM 基类 用于定义数据库模型
# 该类是所有数据库模型的基类，通过继承自它，可以自动获得数据库模型的属性和方法。
Base = declarative_base() # 声明式基类


# 依赖项：获取数据库会话
# 用于在路由处理函数中获取数据库会话实例，用于执行数据库操作。
# 会话实例在路由处理函数执行完成后自动关闭，确保数据库连接被释放。
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()