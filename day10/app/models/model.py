from sqlalchemy import Column, Integer, String, Float
from ..database import Base

class BookModel(Base):
    __tablename__ = 'books'
    id    = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255),unique=True, nullable=False)
    author  = Column(String(100), nullable=False)
    price = Column(Float, nullable=False, default=0)
    quantity = Column(Integer, nullable=False, default=0)
