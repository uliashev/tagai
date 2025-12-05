import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal
import os

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Django settings
    SECRET_KEY: str
    DEBUG: bool = False

    # Database settings
    DB_HOST: str = Field(default="localhost", alias="POSTGRES_HOST")
    DB_PORT: int = Field(default=5432, alias="POSTGRES_PORT")
    DB_NAME: str = Field(default="postgres", alias="POSTGRES_DB")
    DB_USER: str = Field(default="postgres", alias="POSTGRES_USER")
    DB_PASSWORD: str = Field(default="postgres", alias="POSTGRES_PASSWORD")

    # Celery settings
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0", alias="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0", alias="CELERY_RESULT_BACKEND")

    # Environment
    DJANGO_ENV: Literal["local", "docker", "compose"] = "local"

    model_config = SettingsConfigDict(env_file=None, env_file_encoding="utf-8", extra="ignore")

    @classmethod
    def settings_for_env(cls):
        env = os.getenv("DJANGO_ENV", "local")
        logger.info(f"[Pydantic Settings] Loading environment: {env}")
        env_file_map = {
            "local": ".env",
            "docker": ".env.docker",
        }
        env_file = env_file_map.get(env, ".env")
        logger.info(f"[Pydantic Settings] Using environment file: {env_file}")
        return cls(_env_file=env_file)
