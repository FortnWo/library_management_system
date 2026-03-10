import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    """项目启动脚本（统一管理参数）"""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # 允许外部访问
        port=settings.PORT,
        reload=settings.DEBUG,  # 开发热重载，生产关闭
        workers=1 if settings.DEBUG else 4  # 生产多进程
    )