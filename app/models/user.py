from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.associations import user_role_table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    roles = relationship(
        "Role", secondary=user_role_table, back_populates="users"
    )
