from fastapi import APIRouter, Depends
from typing import Annotated
from app.services.auth_service import AuthService
from app.core.db import database
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import (
    UserCreate,
    TokenResponse,
    UserResponse,
)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db_session: Annotated[Session, Depends(database.get_session)],
):
    """
    Register a new user.
    """
    service = AuthService(db_session)
    return service.register_user(user)


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(database.get_session),
):
    """
    Authenticate a user and return a token.
    """
    auth_service = AuthService(db_session)
    user = auth_service.authenticate_user(
        credentials.username, credentials.password
    )
    return auth_service.create_token(user)
