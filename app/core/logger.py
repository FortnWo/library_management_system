import logging
from logging.handlers import RotatingFileHandler
import os
from app.core.config import settings

# 创建日志目录
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 配置日志器
logger = logging.getLogger(settings.PROJECT_NAME)
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
logger.propagate = False  # 避免重复输出

# 日志格式
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

# 1. 控制台处理器（输出到终端）
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 2. 文件处理器（输出到文件，按大小切割）
file_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIR, "app.log"),
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,  # 保留5个备份
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# 添加处理器
logger.addHandler(console_handler)
logger.addHandler(file_handler)