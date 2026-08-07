from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schema import BaseModel, BookCreate, BookUpdate, BookResponse
from app.services.service import create_book, get_all_books, get_book_by_id, update_book, delete_book, search_books, get_top_borrowed_books, get_borrow_warning_books

router = APIRouter(tags=['Library'], prefix='/api/v1/books')

class JSONResponse(BaseModel):
    message: str
    code: int
    data: BookResponse

@router.post('', response_model=JSONResponse)
def add_book(book_data: BookCreate, db: Session = Depends(get_db)):
    result = create_book(book_data=book_data.model_dump(), db=db)
    if result:
        return {
            'message': 'Thêm sách thành công',
            'code': 201,
            'data': result
        }
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Thêm sách thất bại')

@router.get('', response_model=list[BookResponse])
def show_all_books(db: Session = Depends(get_db)):
    return get_all_books(db)

@router.get('/search')
def search_books_endpoint(
        query: str = Query(..., min_length=1, description="Từ khóa tìm kiếm theo tiêu đề, tác giả hoặc thể loại"),
        db: Session = Depends(get_db)
):
    results = search_books(query=query, db=db)
    if results:
        return {
            "message": f"Tìm thấy {len(results)} kết quả phù hợp",
            "code": status.HTTP_200_OK,
            "data": results
        }
    return {
        "message": f"Tìm thấy {len(results)} kết quả phù hợp",
        "code": status.HTTP_404_NOT_FOUND,
        "data": results
    }

@router.get('{book_id}', response_model=BookResponse)
def show_book_by_id(book_id: int, db: Session = Depends(get_db)):
    return get_book_by_id(book_id=book_id, db=db)

@router.put('{book_id}', response_model=JSONResponse)
def edit_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    return {'message': 'Cập nhật thành công',
            'code': status.HTTP_200_OK,
            'data': update_book(book_id=book_id,book_data=book_data.model_dump(),db=db)
            }

@router.delete('{book_id}')
def remove_book(book_id: int, db: Session = Depends(get_db)):
    if delete_book(book_id=book_id,db=db):
        return {
            'message': 'Xóa thành công'
        }
    return None

@router.get('/borrow-warning')
def borrow_warning_endpoint(
    threshold: int = Query(default=5, ge=0, description="Ngưỡng cảnh báo số lượng sách còn lại"),
    db: Session = Depends(get_db)
):
    books = get_borrow_warning_books(threshold=threshold, db=db)
    return {
        "message": f"Tìm thấy {len(books)} sách có số lượng khả dụng <= {threshold}",
        "code": status.HTTP_200_OK,
        "data": books
    }

@router.get('/top-borrowed')
def top_borrowed_endpoint(
    limit: int = Query(default=5, ge=1, description="Số lượng sách top cần lấy"),
    db: Session = Depends(get_db)
):
    top_books = get_top_borrowed_books(limit=limit, db=db)
    return {
        "message": f"Top {len(top_books)} cuốn sách được mượn nhiều nhất",
        "code": status.HTTP_200_OK,
        "data": top_books
    }