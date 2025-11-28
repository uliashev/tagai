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
    DB_HOST: str = Field(alias="POSTGRES_HOST")
    DB_PORT: int = Field(alias="POSTGRES_PORT")
    DB_NAME: str = Field(alias="POSTGRES_DB")
    DB_USER: str = Field(alias="POSTGRES_USER")
    DB_PASSWORD: str = Field(alias="POSTGRES_PASSWORD")

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
