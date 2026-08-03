from fastapi import FastAPI, HTTPException, status
from app.schemas.schema import BookCreate, BookUpdate

app = FastAPI(title='library_management')

books = [
    {
    "id": 1,
    "ten_sach": "Nhà Giả Kim",
    "tac_gia": "Paulo Coelho",
    "nam_xuat_ban": 1988,
    "so_luong": 5
    },
    {
    "id": 2,
    "ten_sach": "Tôi Thấy Hoa Vàng Trên Cỏ Xanh",
    "tac_gia": "Nguyễn Nhật Ánh",
    "nam_xuat_ban": 2010,
    "so_luong": 10
    },
    {
    "id": 3,
    "ten_sach": "Chí Phèo",
    "tac_gia": "Nam Cao",
    "nam_xuat_ban": 1941,
    "so_luong": 15
    }
]

@app.post('/books')
def add_book(book_data: BookCreate):
    try:
        new_book = book_data.model_dump()
        books.append(new_book)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Them sach that bai')
    else:
        return {
            'message': 'Them sach thanh cong',
            'data': new_book
        }

@app.get('/books')
def show_all_book():
    if len(books) == 0:
        return{
            'message': 'Danh sach rong'
        }
    return books

@app.get('/books/{book_id}')
def find_book_by_id(book_id: int):
    book = next((b for b in books if b['id'] == book_id),None)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Khong tim thay')
    return book

@app.put('/books/{book_id}')
def update_book(book_id: int, book_data: BookUpdate):
    book = find_book_by_id(book_id=book_id)
    for key,val in book_data.model_dump().items():
        book[key] = val
    return book

@app.delete('/books/{book_id}')
def remove_book(book_id: int):
    books.remove(find_book_by_id(book_id=book_id))
    return{'message': 'Xoa thanh cong'}