from fastapi import APIRouter, Depends
from app.schemas.auth import UserCreate, Token
from app.services.auth_service import AuthService
from app.core.db import database
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/register", response_model=Token)
def register_user(
    user: UserCreate, db: Session = Depends(database.get_session)
):
    service = AuthService(db)
    return service.register_user(user)


@router.post("/login", response_model=Token)
def login_user(
    email: str, password: str, db: Session = Depends(database.get_session)
):
    service = AuthService(db)
    return service.authenticate_user(email, password)
