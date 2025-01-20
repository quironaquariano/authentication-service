from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.associations import role_permission_table
from app.models.base import Base


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    roles = relationship(
        "Role",
        secondary=role_permission_table,
        back_populates="permissions",
    )
