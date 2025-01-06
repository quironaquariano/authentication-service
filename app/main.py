from fastapi import FastAPI
from app.routes import auth
from app.core.db import Database
from app.core.config import settings

app = FastAPI()

db = Database(settings.DATABASE_URL)
db.create_tables()

app.include_router(
    auth.router, prefix="/authentication", tags=["Authentication"]
)
