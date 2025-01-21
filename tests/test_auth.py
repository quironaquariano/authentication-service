from fastapi.testclient import TestClient
from passlib.hash import bcrypt
from app.models.user import User
from sqlalchemy.orm import Session


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


class TestAuth:
    """Tests related to Authentication functionality."""

    def test_register_user(self, test_client: TestClient):
        """Test the user registration endpoint."""

        response = test_client.post(
            "/authentication/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword",
            },
        )
        assert (
            response.status_code == 200
        ), f"Unexpected status code: {response.status_code}"

    def test_login_user(self, test_client: TestClient, test_session: Session):
        """Test the user login endpoint"""

        # Create a user
        email = "user-login@a.c"
        password = "user-login-pw"
        create_user(
            test_session, username="user-login", email=email, password=password
        )

        # Login with valid credentials
        response = test_client.post(
            "/authentication/login",
            json={"email": email, "password": password},
        )
        assert (
            response.status_code == 200
        ), f"Unexpected status code: {response.status_code}"
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
