from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings


class Security:
    def __init__(self):
        self.password_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto"
        )
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)

    def hash_password(self, password: str) -> str:
        """Hashes a plain password"""
        return self.password_context.hash(password)

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        """Verifies a plain password against a hashed password"""
        return self.password_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        """
        Creates a JWT access token with the given data.

        Args:
            data (dict): The data to encode in the token.

        Returns:
            str: Encoded JWT Token
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    def decode_access_token(self, token: str) -> dict:
        """
        Decodes and validates a JWT access token.

        Args:
            token (str): Encoded JWT token.

        Returns:
            dict: Decoded token payload.

        Raises:
            JWTError: If the token is invalid or expired.
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError as e:
            raise ValueError("Invalid or expired token") from e


security = Security()
