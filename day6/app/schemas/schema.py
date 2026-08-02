from pydantic import BaseModel

class BookCreate(BaseModel):
    id: int
    title: str
    author: str
    price: float
    pages: int

class BookResponse(BookCreate):
    id: int
