from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.book import book as crud_book
from app.db.session import get_db
from app.schemas.book import BookCreate, BookUpdate, BookResponse, BookListResponse
from app.core.logger import logger

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookResponse, summary="创建图书")
def create_book(
    book_in: BookCreate,
    db: Session = Depends(get_db)
):
    """创建新图书"""
    try:
        # 可选：校验书名唯一性
        if crud_book.get_by_title(db, title=book_in.title):
            raise HTTPException(status_code=400, detail="该图书已存在")
        
        db_book = crud_book.create(db, obj_in=book_in)
        logger.info(f"创建图书成功：{db_book.title}（ID：{db_book.id}）")
        return db_book
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"创建图书失败：{str(e)}")
        raise HTTPException(status_code=500, detail="创建图书失败")

@router.get("/{book_id}", response_model=BookResponse, summary="获取单个图书")
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取图书"""
    db_book = crud_book.get(db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="图书不存在")
    return db_book

@router.get("/", response_model=BookListResponse, summary="获取图书列表")
def get_books(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """分页获取图书列表"""
    books = crud_book.get_multi(db, skip=skip, limit=limit)
    return {"code": 200, "msg": "success", "data": books}

@router.put("/{book_id}", response_model=BookResponse, summary="更新图书")
def update_book(
    book_id: int,
    book_in: BookUpdate,
    db: Session = Depends(get_db)
):
    """更新图书信息"""
    db_book = crud_book.get(db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="图书不存在")
    
    # 若更新书名，校验唯一性
    if book_in.title and book_in.title != db_book.title:
        if crud_book.get_by_title(db, title=book_in.title):
            raise HTTPException(status_code=400, detail="该图书已存在")
    
    db_book = crud_book.update(db, db_obj=db_book, obj_in=book_in)
    logger.info(f"更新图书成功：{db_book.title}（ID：{db_book.id}）")
    return db_book

@router.delete("/{book_id}", response_model=BookResponse, summary="删除图书")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """删除图书"""
    db_book = crud_book.get(db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="图书不存在")
    db_book = crud_book.remove(db, id=book_id)
    logger.info(f"删除图书成功：{db_book.title}（ID：{db_book.id}）")
    return db_book