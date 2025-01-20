from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.models.associations import role_permission_table, user_role_table
from app.models.base import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False, index=True)

    permissions = relationship(
        "Permission", secondary=role_permission_table, back_populates="roles"
    )
    users = relationship(
        "User", secondary=user_role_table, back_populates="roles"
    )
