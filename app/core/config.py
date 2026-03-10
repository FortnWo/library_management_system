from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # 项目基础配置
    PROJECT_NAME: str = "LibraryManagementSystem"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    PORT: int = 8000

    # MySQL数据库配置（从.env读取）
    DB_URL: str = "mysql+pymysql://library_user:123456@localhost:3306/library_management?charset=utf8mb4"

    # 安全配置
    SECRET_KEY: str = "default-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 加载.env文件（优先级：环境变量 > .env > 默认值）
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False  # 不区分环境变量大小写
    )

# 全局配置实例（全项目复用）
settings = Settings()