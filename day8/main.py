from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import db_init, Base, engine, get_db
from app.schemas.schema import BookCreate, BookResponse, BaseModel
from app.models.model import BookModel

db_init()
Base.metadata.create_all(bind=engine)

app = FastAPI(title='library_management')

class JSONResponse(BaseModel):
    message: str
    data: BookResponse

@app.post('/books', response_model=JSONResponse)
def add_book(book_data: BookCreate, db: Session = Depends(get_db)):
    code_existed = db.query(BookModel).filter_by(code=book_data.code).first()
    if code_existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='code da ton tai')
    try:
        new_book = BookModel(**book_data.model_dump())
        db.add(new_book)
        db.flush()
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Them sach that bai')
    else:
        db.commit()
        db.refresh(new_book)
        return {'message':'them sach thanh cong',
                'data':new_book}

@app.get('/books', response_model=list[BookResponse])
def show_books(db: Session = Depends(get_db)):
    book_list = db.query(BookModel).all()
    if not book_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Danh sach rong')
    return book_list