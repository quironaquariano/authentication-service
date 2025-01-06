from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings


class Security:
    def __init__(self):
        self.password_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto"
        )

    def hash_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return self.password_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )


security = Security()
