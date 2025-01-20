import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, database
from app.models.base import Base

# Configure test database
db_path = r"tests/test.db"
TEST_DATABASE_URL = f"sqlite:///{db_path}"


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Set up the test database: create tables and override dependencies.
    """
    # Reconfigure the database instance for testing
    database.configure(TEST_DATABASE_URL)

    test_engine = create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    database.engine = test_engine

    test_session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    database.session_local = test_session_local

    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    yield database

    # Drop all tables after tests
    Base.metadata.drop_all(bind=test_engine)

    # Remove the test database file
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope="function")
def test_client():
    """
    Create a FastAPI test client configured to use the test database.
    """
    client = TestClient(app)
    yield client
