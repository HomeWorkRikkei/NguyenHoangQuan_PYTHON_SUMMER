from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.model import BookModel

def create_book(book_data: dict, db: Session):
    title_existed = db.query(BookModel).filter(BookModel.title == book_data['title']).first()
    if title_existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Sach da ton tai')

    try:
        new_book = BookModel(**book_data)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except Exception as e:
        db.rollback()
        return None

def delete_book(book_id: int, db: Session):
    book_founded = find_book(book_id, db=db)

    if book_founded:
        db.delete(book_founded)
        db.commit()
        return True
    else:
        return None

def find_book(book_id: int, db: Session):
    book_founded = db.get(BookModel, book_id)
    if book_founded:
        return book_founded
    else:
        return None

def show_books(db: Session):
    book_list = db.query(BookModel).all()
    return book_list

def update_book(book_id: int, book_data: dict, db: Session):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        return None

    update_dict = book_data
    
    for key, value in update_dict.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book