from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models.model import BookModel

def create_book(book_data: dict, db: Session):
    title_existed = db.query(BookModel).filter(BookModel.title == book_data['title']).first()
    if title_existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Sách đã tồn tại')

    try:
        new_book = BookModel(**book_data)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except Exception as e:
        db.rollback()
        print(e)
        return None

def get_all_books(db: Session):
    book_list = db.query(BookModel).all()
    if not book_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Danh sách rỗng')
    return book_list

def get_book_by_id(book_id: int, db: Session):
    book = db.get(BookModel, book_id)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Không tìm thấy sách')

def update_book(book_id: int, book_data: dict, db: Session):
    book = get_book_by_id(book_id=book_id, db=db)
    if book:
        for key,val in book_data.items():
            setattr(book,key,val)
        db.commit()
        db.refresh(book)
        return book
    return  None

def delete_book(book_id: int, db: Session):
    book = get_book_by_id(book_id=book_id,db=db)
    if book:
        db.delete(book)
        db.commit()
        return True
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Không tìm thấy sách')


def search_books(query: str, db: Session):
    search_pattern = f"%{query}%"

    return db.query(BookModel).filter(
        or_(
            BookModel.title.ilike(search_pattern),
            BookModel.author.ilike(search_pattern),
            BookModel.category.ilike(search_pattern)
        )
    ).all()

def get_borrow_warning_books(threshold: int, db: Session):
    return db.query(BookModel).filter(BookModel.available_quantity <= threshold).all()

def get_top_borrowed_books(limit: int, db: Session):
    return db.query(BookModel).order_by(BookModel.borrow_count.desc()).limit(limit).all()