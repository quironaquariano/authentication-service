from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    RESET_PASSWORD_TOKEN_EXPIRE_MINUTES: int
    TOKEN_URL: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    FRONTEND_URL: str
    SMTP_FROM_EMAIL: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()
