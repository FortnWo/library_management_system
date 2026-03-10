from sqlalchemy import Column, Integer, String
from app.models.base import BaseModel

class Book(BaseModel):
    """图书模型（MySQL适配）"""
    __tablename__ = "books"

    title = Column(String(100), index=True, comment="书名")
    author = Column(String(50), comment="作者")
    publisher = Column(String(100), comment="出版社")
    stock = Column(Integer, default=0, comment="库存")