from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy_utils import create_database, database_exists

engine = create_engine('mysql+pymysql://API_db:123456@localhost:3306/library_db')
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase): pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def db_init():
    if not database_exists(engine.url):
        create_database(engine.url)