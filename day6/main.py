from fastapi import FastAPI, HTTPException, status
from app.schemas.schema import BookCreate, BookResponse

app = FastAPI(title='library_management ')

books = []

@app.post('/books')
def add_book(book_data: BookCreate):
    try:
        new_book = book_data.model_dump()
        books.append(new_book)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Them that bai')
    else:
        return {
            'message': 'them thanh cong',
            'data': new_book
        }

@app.get('/books')
def search_book(book_id: int):
    book = [item for item in books if item['id'] == book_id]
    if book:
        return book
    else:
        return {
            "detail": "Book not found"
        }