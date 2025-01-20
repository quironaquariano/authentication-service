from fastapi import FastAPI
from app.routes import auth
from app.routes import rbac
from app.core.db import database
from app.core.config import settings

app = FastAPI()

# Create a database instance and configure it
database.configure(settings.DATABASE_URL)

# Initialize production database
database.create_tables()


# Include routers
app.include_router(
    auth.router, prefix="/authentication", tags=["Authentication"]
)
app.include_router(rbac.router, prefix="/rbac", tags=["RBAC"])
