from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    #    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/postgres"
    database_url: str = "sqlite://"
    echo: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class Settings(BaseSettings):
    api_prefix: str = "api/v1"
    db: DBSettings = DBSettings()
    secret_key: str = "secret_key"
    algorithm: str = "HS256"


settings = Settings()
