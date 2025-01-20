from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import security
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.db import database


class AuthDependencies:
    def ge_current_user(
        self,
        token: str = Depends(security.oauth2_scheme),
        db: Session = Depends(database.get_session),
    ) -> User:
        """Retrive the currently authenticated user based on JWT token.

        Args:
            token (str, optional): The JWT token from the request's authorization header. Defaults to Depends(security.oauth2_scheme).
            db (Session, optional): The Database session. Defaults to Depends(database.get_session).

        Returns:
            User: The authrorized user object

        Raises:
            HTTPException: If token is invalid or the user is not found.
        """

        try:
            payload = security.decode_access_token(token)
            user_email: str = payload.get("sub")
            if not user_email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Inavlid token: subject (sub) missing",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Retrive user from database
        self.user_repo = UserRepository(db)
        user = self.user_repo.get_by_email(user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user


auth_dependencies = AuthDependencies()
