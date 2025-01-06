# Configuração para Testes
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.db import Database
from app.main import app

# Configurar o banco de dados de teste
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_database():
    """Configura um banco de dados de teste com SQLite em memória."""
    test_engine = create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )

    test_db = Database(TEST_DATABASE_URL)
    test_db.engine = test_engine
    test_db.session_local = TestSessionLocal

    # Criar as tabelas no banco de teste
    test_db.create_tables()
    yield test_db
    # Remover as tabelas após o teste
    test_db.drop_tables()


@pytest.fixture(scope="function")
def db_session(test_database):
    """Gera uma sessão do banco de dados para os testes."""
    db = test_database.get_session()
    yield from db


@pytest.fixture(scope="session", autouse=True)
def override_database_dependency():
    """
    Sobrescreve a dependência de banco de dados para o escopo de sessão de teste.
    """
    test_database_url = "sqlite:///:memory:"
    test_database = Database(test_database_url)

    def override_get_session():
        yield from test_database.get_session()

    # Substituir a dependência no FastAPI
    app.dependency_overrides[Database.get_session] = override_get_session


@pytest.fixture(scope="function")
def test_client():
    """
    Gera um cliente de teste do FastAPI, configurado para usar o banco de dados de teste.
    """
    # Configurar o banco de dados de teste
    test_database_url = "sqlite:///:memory:"
    test_database = Database(test_database_url)

    # Criar as tabelas no banco de teste
    test_database.create_tables()

    def override_get_session():
        yield from test_database.get_session()

    # Substituir a dependência no FastAPI
    app.dependency_overrides[Database.get_session] = override_get_session

    # Retornar o cliente de teste
    client = TestClient(app)
    yield client

    # Limpar o banco após os testes
    test_database.drop_tables()
