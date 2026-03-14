from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    model_config = ConfigDict(
        env_file=".env.local",
        extra="ignore"
    )


settings = Settings()
