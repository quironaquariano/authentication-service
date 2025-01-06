from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService
from app.core.db import Database
from sqlalchemy.orm import Session
from app.core.config import settings
from app.schemas.auth import (
    UserCreate,
    RegisterResponse,
    LoginRequest,
    TokenResponse,
)


router = APIRouter()
db = Database(settings.DATABASE_URL)


@router.post("/register", response_model=RegisterResponse)
def register_user(
    user: UserCreate,
    db_session: Session = Depends(db.get_session),
):
    service = AuthService(db_session)
    return service.register_user(user)


@router.post("/login", response_model=TokenResponse)
def login_user(
    credentials: LoginRequest,
    db_session: Session = Depends(db.get_session),
):
    service = AuthService(db_session)
    return service.authenticate_user(credentials)
