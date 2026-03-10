from pydantic import Field
from app.schemas.base import BaseSchema, BaseResponse
from datetime import datetime

# 请求模型
class BookCreate(BaseSchema):
    title: str = Field(..., min_length=1, max_length=100, description="书名")
    author: str = Field(..., max_length=50, description="作者")
    publisher: str = Field(..., max_length=100, description="出版社")
    stock: int = Field(0, ge=0, description="库存（非负）")

class BookUpdate(BaseSchema):
    title: str | None = Field(None, min_length=1, max_length=100)
    author: str | None = Field(None, max_length=50)
    publisher: str | None = Field(None, max_length=100)
    stock: int | None = Field(None, ge=0)

# 响应模型
class BookResponse(BaseSchema):
    id: int
    title: str
    author: str
    publisher: str
    stock: int
    created_at: datetime

# 列表响应模型
class BookListResponse(BaseResponse):
    data: list[BookResponse]