from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schema import BookResponse, BaseModel, BookCreate, BookUpdate
from app.services.service import create_book, delete_book, find_book, show_books, update_book

router = APIRouter(tags=['Books'], prefix='/books')

class JSONResponse(BaseModel):
    message: str
    data: BookResponse

@router.post('/books',tags=['Books'], response_model=JSONResponse)
def add_book(book_data: BookCreate, db: Session = Depends(get_db)):
    result = create_book(book_data=book_data.model_dump(), db=db)
    if result:
        return{'message': 'Them sach thanh cong',
               'data': result}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Them sach that bai')

@router.delete('/books/{book_id}', tags=['Books'])
def remove_book(book_id: int, db: Session = Depends(get_db)):
    result = delete_book(book_id=book_id, db=db)
    if result:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='Xoa thanh cong')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Xoa that bai')

@router.get('/books', tags=['Books'], response_model=list[BookResponse])
def get_all_book(db: Session=Depends(get_db)):
    result = show_books(db=db)
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Danh sach rong')

@router.get('/books/{book_id}', tags=['Books'], response_model=BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    result = find_book(book_id=book_id, db=db)
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Khong tim thay sach')

@router.patch('/books/{book_id}', tags=['Books'])
def update_book_endpoint(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    updated_book = update_book(book_id=book_id, book_data=book_data.model_dump(), db=db)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Không tìm thấy sách")
        
    return {'message': 'Cập nhật thành công', 'data': updated_book}