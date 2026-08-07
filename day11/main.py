from fastapi import FastAPI
from app.routers.router import router
from app.database import db_init, engine, Base

db_init()
Base.metadata.create_all(bind=engine)

app = FastAPI(title='Library Manage')

app.include_router(router)