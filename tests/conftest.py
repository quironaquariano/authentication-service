import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, database
from app.models.base import Base

# Configure test database
# Use SQLite file database for testing
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Set up the test database: create tables and override dependencies.
    This fixture runs once per test session.
    """
    # Reconfigure the database instance for testing
    database.configure(TEST_DATABASE_URL)

    # Create a test engine with SQLite file database
    test_engine = create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    database.engine = test_engine

    # Create a sessionmaker for the test database
    test_session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    database.session_local = test_session_local

    # Create all tables in the test database
    Base.metadata.create_all(bind=test_engine)

    # Yield the database instance to the tests
    yield database

    # Drop all tables after tests (cleanup)
    Base.metadata.drop_all(bind=test_engine)

    # Remove the test database file
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture
def test_session(setup_test_database):
    """
    Provide a database session for each test function.
    This fixture ensures the session is properly closed after each test.
    """
    session = setup_test_database.session_local()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def test_client():
    """
    Create a FastAPI test client configured to use the test database.
    This fixture is scoped to each test function.
    """
    client = TestClient(app)
    yield client
