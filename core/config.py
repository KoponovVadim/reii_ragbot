from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, EmailStr
from typing import Optional


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    DATABASE_URL: Optional[PostgresDsn] = None

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: EmailStr

    APP_NAME: str = "Chat Assistent"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return str(self.DATABASE_URL)
        return f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()
