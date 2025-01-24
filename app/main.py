from fastapi import FastAPI
from app.api.v1.routes import auth, rbac, password
from app.core.db import database
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

# Create a database instance and configure it
database.configure(settings.DATABASE_URL)

# Initialize production database
if not settings.TESTING:
    database.create_tables()

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(rbac.router, prefix="/api/v1/users", tags=["users"])
app.include_router(
    password.router, prefix="/api/v1/auth", tags=["password recovery"]
)
