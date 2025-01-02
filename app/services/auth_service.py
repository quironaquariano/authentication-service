from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.core.security import security
from app.schemas.auth import UserCreate, Token


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(self, user: UserCreate) -> Token:
        if self.user_repo.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        hashed_password = security.hash_password(user.pawwsord)
        new_user = self.user_repo.create(
            user.username, user.email, hashed_password
        )
        token = security.create_access_token({"sub": new_user})
        return Token(access_token=token, token_type="bearer")

    def authenticate_user(self, email: str, password: str) -> Token:
        user = self.user_repo.get_by_email(email)
        if not user or not security.verify_password(
            password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentilas",
            )
        token = security.create_access_token({"sub": user.email})
        return Token(access_token=token, token_type="bearer")
