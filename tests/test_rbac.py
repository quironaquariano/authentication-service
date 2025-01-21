import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User
from passlib.hash import bcrypt

# Constants
USERNAME = "user1"
USER_EMAIL = "user1@ex.co"
USER_PASSWORD = "user1pw"
PROTECTED_ENDPOINT = "/rbac/protected-endpoint"


# Helpers
def create_user(
    session: Session, username: str, email: str, password: str
) -> User:
    """Helper to Create or retrieve a user in the database."""
    user = session.query(User).filter_by(email=email).first()
    if user is None:
        user = User(
            username=username,
            email=email,
            hashed_password=bcrypt.hash(password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def create_role(session: Session, name: str) -> Role:
    """Helper to Create or retrieve a Role in the database."""
    role = session.query(Role).filter_by(name=name).first()
    if role is None:
        role = Role(name=name)
        session.add(role)
        session.commit()
        session.refresh(role)
    return role


def create_permission(session: Session, name: str) -> Permission:
    """Helper to Create or retrieve a Permission in the database."""
    permission = session.query(Permission).filter_by(name=name).first()
    if permission is None:
        permission = Permission(name=name)
        session.add(permission)
        session.commit()
        session.refresh(permission)
    return permission


def create_role_with_permissions(
    session: Session, role_name: str, permissions: list[str]
) -> Role:
    """Helper to Create a role and assign permissions."""
    role = session.query(Role).filter_by(name=role_name).first()
    if role is None:
        role = Role(name=role_name)
        session.add(role)
        session.commit()

    for permission_name in permissions:
        permission = (
            session.query(Permission).filter_by(name=permission_name).first()
        )
        if permission is None:
            permission = Permission(name=permission_name)
            session.add(permission)
            session.commit()
        if permission not in role.permissions:
            role.permissions.append(permission)

    session.commit()
    session.refresh(role)
    return role


def authenticate_user(
    test_client: TestClient, email: str, password: str
) -> str:
    """Authenticate a user and return the access token."""
    response = test_client.post(
        url="/authentication/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json().get("access_token")


def assign_role_to_user(session: Session, user: User, role: Role):
    """Helper function assign specific Role to specific User"""

    if role not in user.roles:
        user.roles.append(role)
        session.commit()
        session.refresh(user)

    return user


# Fixtures


@pytest.fixture
def test_authenticated_user(test_client: TestClient, test_session: Session):
    user = create_user(
        session=test_session,
        username=USERNAME,
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )
    role = create_role_with_permissions(
        session=test_session,
        role_name="admin",
        permissions=["creator", "viewer", "editor", "developer"],
    )

    assign_role_to_user(test_session, user, role)
    token = authenticate_user(test_client, USER_EMAIL, USER_PASSWORD)
    test_client.headers.update({"Authorization": f"Bearer {token}"})
    return test_client


# Tests
class TestRBAC:
    """Tests related to RBAC functionality."""

    def test_access_protected_endpoint(
        self, test_authenticated_user: TestClient
    ):
        response = test_authenticated_user.get(PROTECTED_ENDPOINT)
        assert (
            response.status_code == 200
        ), f"Unexpected response: {response.text}"
        assert response.json().get("message") == "Permission granted"

    def test_access_protected_endpoint_no_permission(
        self, test_client: TestClient, test_session: Session
    ):
        user = create_user(
            test_session,
            username="user_no_permission",
            email="no_permission@ex.com",
            password="nopermissionpw",
        )
        role = create_role_with_permissions(
            session=test_session,
            role_name="guest",
            permissions=["read-only"],
        )
        assign_role_to_user(test_session, user, role)
        token = authenticate_user(
            test_client, "no_permission@ex.com", "nopermissionpw"
        )
        test_client.headers.update({"Authorization": f"Bearer {token}"})
        response = test_client.get(PROTECTED_ENDPOINT)
        assert response.status_code == 403
        assert response.json().get("detail") == "Permission denied"

    def test_user_not_authenticated(self, test_client: TestClient):
        response = test_client.get(PROTECTED_ENDPOINT)
        assert response.status_code == 401
        assert response.json().get("detail") == "Not authenticated"

    def test_create_role(self, test_authenticated_user: TestClient):
        response = test_authenticated_user.post(
            "/rbac/create-role", params={"name": "test-role"}
        )
        assert response.status_code == 200

    def test_create_permissions(self, test_authenticated_user: TestClient):
        response = test_authenticated_user.post(
            "/rbac/create-permission",
            params={"name": ["permission-test-1", "permission-test-2"]},
        )
        assert response.status_code == 200

    def test_assign_role_permission(
        self, test_authenticated_user: TestClient, test_session: TestClient
    ):

        role = create_role(test_session, "assign-permission-role")
        permission = create_permission(test_session, "assign-permission")
        permission2 = create_permission(test_session, "assign-permission2")

        response = test_authenticated_user.post(
            "/rbac/assign-permissions",
            json={
                "role_name": role.name,
                "permission_name": [permission.name, permission2.name],
            },
        )

        print(response.content)
        assert response.status_code == 200

    def test_assign_user_role(
        self, test_authenticated_user: TestClient, test_session: Session
    ):
        user = create_user(
            test_session,
            username="specific-user",
            email="specific-user@a.c",
            password="specific-user-pw",
        )
        role = create_role(test_session, "specific-user-role")

        response = test_authenticated_user.post(
            url="/rbac/assign-role",
            json={"user_email": user.email, "role_name": role.name},
        )
        print(response.json())
        assert response.status_code == 200
        assert response.json().get("message") == "Role assigned successfully"
