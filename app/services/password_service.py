from datetime import datetime, timedelta, timezone
import secrets
from sqlalchemy.orm import Session
from app.core.security import security
from app.core.config import settings
from app.dependecies.email import EmailService
from app.models.token import PasswordResetToken
from app.models.user import User
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository


class PasswordService:
    def __init__(self, db: Session):
        self.token_repository = TokenRepository(db)
        self.user_repository = UserRepository(db)
        self.email_service = EmailService()

    def generate_reset_token(self, user: User) -> str:
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.RESET_PASSWORD_TOKEN_EXPIRE_MINUTES
        )
        reset_token = PasswordResetToken(
            user_id=user.id, token=token, expires_at=expires_at
        )
        self.token_repository.create(reset_token)
        return token

    def send_reset_password_email(self, user: User, token: str) -> None:
        subject = "Password Reset"
        body = f"""
        <h1>Password Reset</h1>
        <p>Hello {user.fullname}.</>
        <p>
            You have requested to reset your password. Click the link below to reset your password.
        </p>
        <p><a href="{settings.FRONTEND_URL}/reset-password?token={token}">Reset Password</a></p>
        <p>If you did not request this, please ignore this email.</p>
        """
        self.email_service.send_email(user.email, subject, body)

    def validate_reset_token(self, token: str) -> PasswordResetToken | None:
        reset_token = self.token_repository.get_by_token(token)

        if not reset_token or reset_token.status != "active":
            return None

        if reset_token.expires_at.tzinfo is None:
            reset_token.expires_at = reset_token.expires_at.replace(
                tzinfo=timezone.utc
            )

        if reset_token.expires_at < datetime.now(timezone.utc):
            reset_token.status = "expired"
            self.token_repository.update(reset_token)
            return None

        reset_token.status = "used"
        self.token_repository.update(reset_token)
        return reset_token

    def reset_password(self, token: str, new_password: str) -> bool:
        token = self.validate_reset_token(token)
        if not token:
            return False
        user = self.user_repository.get_by_id(token.user_id)
        if not user:
            return False
        user.hashed_password = security.hash_password(new_password)
        self.token_repository.delete(token)
        self.user_repository.update(user)
        return True
