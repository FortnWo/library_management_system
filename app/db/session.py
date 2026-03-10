from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 创建MySQL引擎（适配连接池，生产级配置）
engine = create_engine(
    settings.DB_URL,
    # MySQL连接池配置（关键！避免频繁创建连接）
    pool_size=10,          # 核心连接数
    max_overflow=20,       # 最大溢出连接数
    pool_recycle=3600,     # 连接回收时间（1小时）
    pool_pre_ping=True,    # 每次请求前检查连接是否有效
    echo=settings.DEBUG    # 开发环境打印SQL，生产关闭
)

# 创建会话工厂（每次请求新建会话）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础模型类（所有ORM模型继承）
Base = declarative_base()

# 依赖函数：获取数据库会话（FastAPI依赖注入）
def get_db():
    db = SessionLocal()
    try:
        yield db  # 提供会话给接口使用
    finally:
        db.close()  # 请求结束关闭会话