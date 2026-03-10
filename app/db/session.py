# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # 导入 DeclarativeBase
from app.core.config import settings

# 新版：定义 Base 为继承 DeclarativeBase 的类，而非 declarative_base() 的返回值
class Base(DeclarativeBase):
    pass

# 创建 MySQL 引擎（保持不变）
engine = create_engine(
    settings.DB_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖函数 get_db 保持不变
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()