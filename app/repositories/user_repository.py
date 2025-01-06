from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserResponse


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, username: str, email: str, hashed_password: str
    ) -> UserResponse:
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
