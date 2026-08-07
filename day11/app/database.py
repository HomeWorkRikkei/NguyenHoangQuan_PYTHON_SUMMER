from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from uvicorn.loops import auto

engine = create_engine('mysql+pymysql://API_db:123456@localhost:3306/library_db_v2')
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase): pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def db_init():
    if not database_exists(engine.url):
        create_database(engine.url)