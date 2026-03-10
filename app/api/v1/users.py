from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.user import user as crud_user
from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.core.logger import logger

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, summary="创建用户")
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """创建新用户（校验用户名/邮箱唯一性）"""
    try:
        # 检查用户名是否存在
        if crud_user.get_by_username(db, username=user_in.username):
            raise HTTPException(status_code=400, detail="用户名已存在")
        # 检查邮箱是否存在
        if crud_user.get_by_email(db, email=user_in.email):
            raise HTTPException(status_code=400, detail="邮箱已存在")
        
        db_user = crud_user.create(db, obj_in=user_in)
        logger.info(f"创建用户成功：{db_user.username}（ID：{db_user.id}）")
        return db_user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"创建用户失败：{str(e)}")
        raise HTTPException(status_code=500, detail="创建用户失败")

@router.get("/{user_id}", response_model=UserResponse, summary="获取单个用户")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取用户"""
    db_user = crud_user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.get("/", response_model=UserListResponse, summary="获取用户列表")
def get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """分页获取用户列表"""
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return {"code": 200, "msg": "success", "data": users}

@router.put("/{user_id}", response_model=UserResponse, summary="更新用户")
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    db_user = crud_user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 若更新用户名/邮箱，校验唯一性
    if user_in.username and user_in.username != db_user.username:
        if crud_user.get_by_username(db, username=user_in.username):
            raise HTTPException(status_code=400, detail="用户名已存在")
    if user_in.email and user_in.email != db_user.email:
        if crud_user.get_by_email(db, email=user_in.email):
            raise HTTPException(status_code=400, detail="邮箱已存在")
    
    db_user = crud_user.update(db, db_obj=db_user, obj_in=user_in)
    logger.info(f"更新用户成功：{db_user.username}（ID：{db_user.id}）")
    return db_user

@router.delete("/{user_id}", response_model=UserResponse, summary="删除用户")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """删除用户"""
    db_user = crud_user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db_user = crud_user.remove(db, id=user_id)
    logger.info(f"删除用户成功：{db_user.username}（ID：{db_user.id}）")
    return db_user