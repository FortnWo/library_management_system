from datetime import datetime

from pydantic import EmailStr, Field, constr

from app.schemas.base import BaseSchema, BaseResponse


# 请求模型（创建/更新用户）
class UserCreate(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    # 使用 constr 进行长度控制，避免超长密码
    password: constr(min_length=6, max_length=128) = Field(..., description="密码")


class UserUpdate(BaseSchema):
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: constr(min_length=6, max_length=128) | None = Field(None, description="密码")

# 响应模型（隐藏敏感字段）
class UserResponse(BaseSchema):
    id: int
    username: str
    email: str
    created_at: datetime

# 列表响应模型
class UserListResponse(BaseResponse):
    data: list[UserResponse]