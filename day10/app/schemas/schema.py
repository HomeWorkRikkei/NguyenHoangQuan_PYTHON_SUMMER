from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    quantity: int

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float
    quantity: int

    model_config = {
        'from_attributes': True
    }

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None