from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # 项目基础配置
    PROJECT_NAME: str = "LibraryManagementSystem"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    PORT: int = 8000

    # 数据库配置
    DB_URL: str = "sqlite:///./library.db"

    # 安全配置
    SECRET_KEY: str = "default-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 加载 .env 文件（优先级：环境变量 > .env > 默认值）
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False  # 不区分大小写，方便使用
    )

# 全局配置实例（整个项目复用）
settings = Settings()