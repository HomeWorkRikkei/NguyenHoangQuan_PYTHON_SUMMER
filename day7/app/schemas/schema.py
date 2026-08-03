from pydantic import BaseModel

class BookCreate(BaseModel):
    id: int
    ten_sach : str
    tac_gia : str
    nam_xuat_ban : int
    so_luong : int

class BookUpdate(BookCreate): pass