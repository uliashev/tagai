import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
import os

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Django settings
    SECRET_KEY: str
    DEBUG: bool = False

    # Database settings
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Environment
    DJANGO_ENV: Literal["local", "docker", "compose"] = "local"

    model_config = SettingsConfigDict(env_file=None, env_file_encoding="utf-8")

    @classmethod
    def settings_for_env(cls):
        env = os.getenv("DJANGO_ENV", "local")
        logger.info(f"[Pydantic Settings] Loading environment: {env}")
        env_file_map = {
            "local": ".env.local",
            "docker": ".env.docker",
        }
        env_file = env_file_map.get(env, ".env.local")
        logger.info(f"[Pydantic Settings] Using environment file: {env_file}")
        return cls(_env_file=env_file)
