from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.core.security import security
from app.schemas.auth import (
    UserCreate,
    UserResponse,
    TokenResponse,
    RegisterResponse,
    LoginRequest,
)


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(self, user: UserCreate) -> RegisterResponse:
        if self.user_repo.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        hashed_password = security.hash_password(user.password)
        new_user = self.user_repo.create(
            user.username, user.email, hashed_password
        )
        token = security.create_access_token({"sub": new_user.email})
        return RegisterResponse(
            user=UserResponse.model_validate(new_user),
            access_token=token,
            token_type="bearer",
        )

    def authenticate_user(self, credentials: LoginRequest) -> TokenResponse:
        user = self.user_repo.get_by_email(credentials.email)
        if not user or not security.verify_password(
            credentials.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentilas",
            )
        token = security.create_access_token({"sub": user.email})
        return TokenResponse(access_token=token, token_type="bearer")
