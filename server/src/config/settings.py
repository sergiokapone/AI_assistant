from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_prefix: str = "api/v1"
    database_url: str = "sqlite+aiosqlite:///db.sqlite3"
    db_echo: bool = True
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    llm_api_key: str = "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"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
