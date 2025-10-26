from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # For the FastAPI app
    DATABASE_URL: str

    # For Alembic (running on host)
    ALEMBIC_DATABASE_URL: str

    # For the DB service
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str


# Create a single, global instance of the settings
settings = Settings()
