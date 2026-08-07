from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    category: str
    price: float= Field(ge=0)
    borrow_count: int = Field(ge=0)
    available_quantity: int = Field(ge=0)

class BookUpdate(BaseModel):
    title: Optional[str] | None
    author: Optional[str] | None
    category: Optional[str] | None
    price: Optional[float] | None
    borrow_count: Optional[int] | None
    available_quantity: Optional[int] | None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    category: str
    price: float
    borrow_count: int
    available_quantity: int

    model_config = ConfigDict(from_attributes=True)