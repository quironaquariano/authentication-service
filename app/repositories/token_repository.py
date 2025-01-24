from sqlalchemy.orm import Session
from app.models.token import PasswordResetToken


class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, token: PasswordResetToken) -> PasswordResetToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def get_by_token(self, token: str) -> PasswordResetToken | None:
        return (
            self.db.query(PasswordResetToken)
            .filter(PasswordResetToken.token == token)
            .first()
        )

    def get_by_id(self, token_id: int) -> PasswordResetToken | None:
        return (
            self.db.query(PasswordResetToken)
            .filter(PasswordResetToken.id == token_id)
            .first()
        )

    def delete(self, token: PasswordResetToken) -> None:
        self.db.delete(token)
        self.db.commit()
        return None

    def update(self, token: PasswordResetToken) -> PasswordResetToken | None:
        existing_token = self.get_by_id(token.id)
        if existing_token:
            existing_token.status = token.status
            self.db.commit()
            self.db.refresh(existing_token)
            return existing_token
        return None
