from pydantic import BaseModel, ConfigDict
from datetime import datetime

class BaseSchema(BaseModel):
    """所有校验模型的基础类"""
    model_config = ConfigDict(
        from_attributes=True,  # 支持从ORM对象转换
        populate_by_name=True, # 支持按字段名赋值
        arbitrary_types_allowed=True  # 允许datetime等类型
    )

class BaseResponse(BaseSchema):
    """通用响应模型"""
    code: int = 200
    msg: str = "success"
    data: dict | list | None = None