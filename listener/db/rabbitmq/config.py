from pydantic import BaseSettings
from functools import lru_cache


class RMQSettings(BaseSettings):
    username: str
    password: str
    host: str
    port: str

    class Config:
        env_prefix = "RMQ_"
        env_file = ".env"


@lru_cache
def get_db_settings() -> RMQSettings:
    return RMQSettings()


settings = get_db_settings()
