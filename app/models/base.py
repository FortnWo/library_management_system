from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func
from app.db.session import Base

class BaseModel(Base):
    """所有数据库模型的基础类"""
    __abstract__ = True  # 抽象类，不生成实际表

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")