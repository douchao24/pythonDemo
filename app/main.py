#  整合所有模块，启动服务
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.core.exceptions import (
    BusinessException,
    business_exception_handler,
    global_exception_handler,
    http_exception_handler
)
from app.api.v1 import users_router, auth_router

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化FastApi应用
app = FastAPI(
  title=settings.APP_NAME,
  version=settings.APP_VERSION,
  description="用户管理服务",
  debug=settings.DEBUG
)

# 注册全局异常处理器
# app.add_exception_handler(HTTPException, http_exception_handler)
# 注册全局异常处理器
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# 跨域配置
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"], # 生产环境改具体域名
  allow_credentials=True, # 允许跨域请求携带凭证
  allow_methods=["*"], # 允许所有请求方法
  allow_headers=["*"], # 允许所有请求头
)

# 注册路由
app.include_router(users_router)
app.include_router(auth_router)

# 根路由
@app.get("/")
def root():
  return {"message": f"欢迎使用 {settings.APP_NAME}"}
