from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Данные для подключения к базе
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str

    # Данные для jwt аутентификации
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20

    @property
    def DATABASE_URL(self) -> str:
        """Динамическая сборка асинхронный URL для SQLAlchemy"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    #настройка источника данных
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()