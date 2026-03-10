from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """用户CRUD（继承通用方法）"""
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """根据用户名查询用户"""
        return db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """根据邮箱查询用户"""
        return db.query(User).filter(User.email == email).first()

# 实例化（供接口调用）
user = CRUDUser(User)