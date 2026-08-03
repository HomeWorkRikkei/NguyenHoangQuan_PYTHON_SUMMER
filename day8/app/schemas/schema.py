from pydantic import BaseModel
from decimal import Decimal

class BookCreate(BaseModel):
    code: str
    title: str
    price: Decimal
    pages: int

class BookResponse(BaseModel):
    id: int
    code: str
    title: str
    price: Decimal
    pages: int

    model_config = {
        'from_attributes': True
    }