from passlib.hash import bcrypt
from sqlalchemy import text


def test_register_user(test_client):
    """
    Test the user registration endpoint.
    """
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


def test_login_user(test_client, setup_test_database):
    """
    Test the user login endpoint.
    """
    hashed_password = bcrypt.hash("testpassword")
    query = text(
        "INSERT INTO users (username, email, hashed_password) "
        "VALUES (:username, :email, :hashed_password)"
    )

    # Insert a user directly into the test database
    with next(setup_test_database.get_session()) as db_session:
        db_session.execute(
            query,
            {
                "username": "testuser2",
                "email": "test2@example.com",
                "hashed_password": hashed_password,
            },
        )
        db_session.commit()

    # Login with valid credentials
    response = test_client.post(
        "/authentication/login",
        json={"email": "test2@example.com", "password": "testpassword"},
    )
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
