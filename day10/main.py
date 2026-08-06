from fastapi import FastAPI
from app.database import db_init, Base, engine
from app.routers.router import router

db_init()
Base.metadata.create_all(bind=engine)

app = FastAPI(title='library_management')

app.include_router(router)