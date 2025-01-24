from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, username: str, email: str, hashed_password: str) -> User:
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

    def get_all(self):
        return self.db.query(User).all()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
        return None

    def update(self, user: User) -> User | None:
        existing_user = self.get_by_id(user.id)
        if existing_user:
            existing_user.username = user.username
            existing_user.email = user.email
            existing_user.hashed_password = user.hashed_password
            self.db.commit()
            self.db.refresh(existing_user)
            return existing_user
        return None
