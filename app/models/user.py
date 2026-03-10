from sqlalchemy import Column, String
from app.models.base import BaseModel

class User(BaseModel):
    """用户模型（MySQL适配）"""
    __tablename__ = "users"  # MySQL表名

    username = Column(String(50), unique=True, index=True, comment="用户名")
    email = Column(String(100), unique=True, index=True, comment="邮箱")
    hashed_password = Column(String(100), comment="加密密码")