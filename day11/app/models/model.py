from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class BookModel(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    borrow_count: Mapped[int] = mapped_column(Integer, default=0)
    available_quantity: Mapped[int] = mapped_column(Integer, default=0)