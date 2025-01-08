from fastapi import APIRouter, Depends
from typing import Annotated
from app.services.auth_service import AuthService
from app.core.db import database
from sqlalchemy.orm import Session
from app.schemas.auth import (
    UserCreate,
    RegisterResponse,
    LoginRequest,
    TokenResponse,
)


router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register_user(
    user: UserCreate,
    db_session: Annotated[Session, Depends(database.get_session)],
):
    """
    Register a new user.
    """
    service = AuthService(db_session)
    return service.register_user(user)


@router.post("/login", response_model=TokenResponse)
def login_user(
    credentials: LoginRequest,
    db_session: Session = Depends(database.get_session),
):
    """
    Authenticate a user and return a token.
    """
    service = AuthService(db_session)
    return service.authenticate_user(credentials)
