from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.config import settings
from app.core.logger import logger
from app.db.session import engine, Base
from app.models import user, book  # 导入模型，确保创建表

# 创建MySQL表（首次运行执行）
Base.metadata.create_all(bind=engine)
logger.info("MySQL数据库表创建成功")

print("DEBUG 模式：", settings.DEBUG)
print("docs_url 配置：", "/docs" if settings.DEBUG else None)

# 初始化FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.18.3/swagger-ui-bundle.js",
    swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.18.3/swagger-ui.css",
    swagger_ui_init_oauth={},
    docs_url="/docs" if settings.DEBUG else None,  # 生产关闭Swagger
    redoc_url="/redoc" if settings.DEBUG else None  # 生产关闭ReDoc
)

# CORS配置（生产指定具体域名）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["https://your-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 健康检查
@app.get("/", summary="健康检查")
def root():
    logger.info("健康检查请求")
    return {"code": 200, "msg": f"欢迎使用 {settings.PROJECT_NAME}", "data": None}