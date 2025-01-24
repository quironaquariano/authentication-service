from fastapi.testclient import TestClient
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from app.models.user import User


ROUTE_PREFIX = "/api/v1/auth"
USER_EMAIL = "almerindo.uazela@gmail.com"


# Helper functions
def create_user(session: Session, username: str, email: str, password: str):
    """Helper to create a user on database"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        user = User(
            username=username,
            email=email,
            hashed_password=bcrypt.hash(password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def get_token_by_email(session: Session, email: str):
    """Helper to get the user token by email"""
    user = session.query(User).filter_by(email=email).first()
    return user.password_reset_tokens[0].token


class TestPasswordReset:
    def test_forgot_password(
        self, test_client: TestClient, test_session: Session
    ):
        """Test the password reset functionality."""
        # create a user
        create_user(test_session, "test-rest-user", USER_EMAIL, "password")

        # Test the forgot password endpoint
        response = test_client.post(
            f"{ROUTE_PREFIX}/forgot-password",
            params={"email": USER_EMAIL},
        )
        print(response.json())
        assert (
            response.status_code == 200
        ), f"Unexpected status code: {response.status_code}"

    def test_reset_password(
        self, test_client: TestClient, test_session: Session
    ):
        """Test the reset password functionality."""

        token = get_token_by_email(test_session, USER_EMAIL)

        # Test the reset password endpoint
        response = test_client.post(
            f"{ROUTE_PREFIX}/reset-password",
            json={"token": token, "new_password": "new-password"},
        )
        print(response.json())
        assert (
            response.status_code == 200
        ), f"Unexpected status code: {response.status_code}"
