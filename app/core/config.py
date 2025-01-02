from pydantic_settings import BaseSettings, ConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = ConfigDict(
        env_file="auth_service/.env", env_file_encoding="utf-8"
    )
