from app.crud.base import CRUDBase
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    """图书CRUD"""
    def get_by_title(self, db: Session, title: str) -> Optional[Book]:
        """根据书名查询图书"""
        return db.query(Book).filter(Book.title == title).first()

# 实例化
book = CRUDBook(Book)