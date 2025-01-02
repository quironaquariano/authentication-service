from fastapi import FastAPI
from app.routes import auth
from app.core.db import database

app = FastAPI()

database.create_tables()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
