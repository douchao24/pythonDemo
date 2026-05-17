# 全局异常处理 
# 用于捕获并处理应用程序中的异常，确保应用程序的稳定性和用户体验。
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse # JSON 响应类

# 自定义异常处理
async def http_exception_handler(request: Request, exc: HTTPException):
  return JSONResponse(
    status_code=exc.status_code,
    content={
      "code": exc.status_code,
      "message": exc.detail,
      "data": None
    }
  )


# 自定义业务异常
class BusinessException(HTTPException):
  def __init__(self, code: int, message: str):
    self.code = code
    self.message = message
    super().__init__(status_code=code, detail=message)

# 常用业务异常封装
class NotFoundException(BusinessException):
  def __init__(self, message: str='数据不存在'):
    super().__init__(code=status.HTTP_404_NOT_Found, message=message)

class AuthFailException(BusinessException):
  def __init__(self, message: str='认证失败，用户名或者密码错误'):
    super().__init__(code=status.HTTP_401_UNAUTHORIZED, message=message)

class ForbiddenException(BusinessException):
    def __init__(self, message: str = "无操作权限"):
        super().__init__(code=status.HTTP_403_FORBIDDEN, message=message)

class ParamException(BusinessException):
    def __init__(self, message: str = "参数校验失败"):
        super().__init__(code=status.HTTP_400_BAD_REQUEST, message=message)


# 全局统一响应
def success_response(data=None, message="操作成功"):
  return {
    "code": 200,
    "message": message,
    "data": data
  }

# 捕获自定义业务异常
async def business_exception_handler(request: Request, exc: BusinessException):
  return JSONResponse(
    content={
      "code": exc.code,
      "message": exc.message,
      "data": None
    }
  ) 

# 捕获系统未知异常
async def global_exception_handler(request: Request, exc: BusinessException):
  return JSONResponse(
    status_code=500,
    content={
      "code": 500,
      "message": "服务器内部异常",
      "data": None
    }
  )