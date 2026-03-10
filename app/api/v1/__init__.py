from fastapi import APIRouter
from app.api.v1 import users, books

# 注册所有v1版本接口
api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(books.router)