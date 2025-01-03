# **Auth Service**

O **Auth Service** é um módulo de autenticação independente desenvolvido em **FastAPI**. Ele fornece APIs para registro e login de usuários, além de geração e validação de tokens JWT. Este serviço foi projetado para ser utilizado como um serviço de autenticação em sistemas maiores, como um e-commerce, e será facilmente extensível para incluir controle de acesso (RBAC) no futuro.

---

## 🚀 **Funcionalidades Atuais**

- **Registro de Usuário**  
  Criação de usuários com validação de dados e armazenamento seguro de senhas usando hashing `bcrypt`.

- **Login**  
  Autenticação de usuários com validação de credenciais e geração de tokens JWT para sessões autenticadas.

- **Token JWT**  
  Tokens assinados para autenticação baseada em sessões com suporte a expiração.

---

## 🔮 **Funcionalidades Futuras**

- **Controle de Acessos (RBAC):**  
  Criação de papéis e permissões para usuários, com integração aos endpoints para limitar acessos com base em permissões.

- **Recuperação de Senha:**  
  Endpoints para recuperação e redefinição de senha com envio de e-mail.

- **Integração com Outros Serviços:**  
  Serviços como e-commerce poderão consumir o Auth Service para autenticação e autorização.

---

## 🛠️ **Tecnologias Utilizadas**

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Banco de Dados:** MySQL
- **ORM:** SQLAlchemy
- **Hashing de Senhas:** Passlib (bcrypt)
- **Autenticação:** JWT (JSON Web Tokens)
- **Gerenciamento de Dependências:** Poetry
- **Testes:** Pytest
- **Infraestrutura:** Docker e Docker Compose

---

## 🛑 **Pré-requisitos**

Certifique-se de ter as ferramentas abaixo instaladas:

- Python 3.9+ (recomendado Python 3.11 ou superior)
- Docker e Docker Compose
- Poetry


