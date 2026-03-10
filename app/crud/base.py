# app/crud/base.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.session import Base
from app.schemas.base import BaseSchema

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseSchema)

# 统一的密码哈希上下文：使用 argon2，完全摆脱 bcrypt 的 72 字节限制
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """根据ID获取单条数据"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """分页获取数据"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """创建数据（密码自动加密）"""
        obj_in_data = obj_in.model_dump()
        # 密码加密（如果提供了明文密码）
        if "password" in obj_in_data and obj_in_data["password"] is not None:
            obj_in_data["hashed_password"] = pwd_context.hash(obj_in_data.pop("password"))
        
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """更新数据"""
        # 运行时不要用 TypeVar 做 isinstance 判断，这里按基类判断
        obj_data = obj_in.model_dump() if isinstance(obj_in, BaseSchema) else obj_in
        # 密码加密（如果更新密码）
        if "password" in obj_data and obj_data["password"] is not None:
            obj_data["hashed_password"] = pwd_context.hash(obj_data.pop("password"))
        
        for field in obj_data:
            if obj_data[field] is not None:
                setattr(db_obj, field, obj_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: Any) -> ModelType:
        """删除数据"""
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj