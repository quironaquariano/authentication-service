from sqlalchemy import Column, DateTime, Enum, Integer, String, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(
        Enum("active", "used", "expired", name="token_status"),
        default="active",
    )
    user = relationship("User", back_populates="password_reset_tokens")
