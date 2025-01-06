<<<<<<< HEAD
# microservices-ecomerce-api
=======
# **Auth Service**

The **Auth Service** is a standalone authentication module built with **FastAPI**. It offers robust APIs for user registration, login, and JWT token generation and validation. Designed for seamless integration into larger systems, such as e-commerce platforms, the service is highly extensible, with planned support for role-based access control (RBAC) and other advanced features.

---

## 🚀 **Current Features**

- **User Registration**  
  Create user accounts with robust data validation and secure password hashing using `bcrypt`.

- **Login**  
  Authenticate users by validating credentials and generating JWT tokens for secure sessions.

- **JWT Tokens**  
  Provide signed tokens for session-based authentication with built-in expiration support.

---

## 🔮 **Future Features**

- **Role-Based Access Control (RBAC):**  
  Enable role and permission management to restrict endpoint access based on user roles.

- **Password Recovery:**  
  Provide endpoints for password reset with email integration.

- **Service Integration:**  
  Allow external services, such as e-commerce platforms, to consume the Auth Service for authentication and authorization.

---

## 🛠️ **Technologies Used**

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Password Hashing:** Passlib (bcrypt)
- **Authentication:** JWT (JSON Web Tokens)
- **Dependency Management:** Poetry
- **Testing:** Pytest
- **Infrastructure:** Docker and Docker Compose

---
>>>>>>> F01-implemtent-auth
