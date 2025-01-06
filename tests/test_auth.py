from passlib.hash import bcrypt
from sqlalchemy import text


# def test_register_user(test_client, db_session):
#     """
#     Testa o registro de um novo usuário no sistema.
#     """
#     response = test_client.post(
#         "/authentication/register",
#         json={
#             "username": "testuser1",
#             "email": "test@example1.com",
#             "password": "testpassword",
#         },
#     )
#     print(response.content)
#     assert response.status_code == 200
#     data = response.json()
#     assert "user" in data
#     # assert data["user"]["username"] == "testuser1"
#     # assert data["user"]["email"] == "test@example1.com"
#     assert "access_token" in data
#     assert data["token_type"] == "bearer"


def test_login_user(test_client, db_session):
    """
    Testa o login de um usuário existente no sistema.
    """
    # Criar um hash da senha
    hashed_password = bcrypt.hash("testpassword")
    print(f"Hashed Password: {hashed_password}")  # Depuração

    # Inserir o usuário diretamente no banco de dados
    db_session.execute(
        text(
            "INSERT INTO users (username, email, hashed_password) VALUES (:username, :email, :hashed_password)"
        ),
        {
            "username": "testuser1",
            "email": "test@example1.com",
            "hashed_password": hashed_password,
        },
    )
    db_session.commit()

    # Validar que o usuário foi inserido
    users = db_session.execute(text("SELECT * FROM users")).fetchall()
    print(f"Users in DB: {users}")  # Depuração

    # Fazer login com as credenciais corretas
    response = test_client.post(
        "/authentication/login",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    print(f"Response: {response.json()}")  # Depuração

    assert response.status_code == 200

    # Validar o conteúdo da resposta
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
