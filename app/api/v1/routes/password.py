from fastapi import APIRouter, Depends, HTTPException, status
from app.core.db import database
from sqlalchemy.orm import Session
from app.schemas.auth import ResetPassword
from app.services.password_service import PasswordService

router = APIRouter()


@router.post("/forgot-password")
async def forgot_password(
    email: str, db: Session = Depends(database.get_session)
):
    service = PasswordService(db)

    # Check if the user exists
    user = service.user_repository.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Generate the reset token
    token = service.generate_reset_token(user)

    # Send the reset password email
    service.send_reset_password_email(user, token)
    return {"message": "Password reset email sent"}


@router.post("/reset-password")
async def reset_password(
    data: ResetPassword, db: Session = Depends(database.get_session)
):
    service = PasswordService(db)

    # Reset the password
    if not service.reset_password(data.token, data.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )

    return {"message": "Password reset successfully"}
