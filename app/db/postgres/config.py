from pydantic import BaseSettings


class DBSettings(BaseSettings):
    username: str
    password: str
    database: str
    host: str
    port: str

    class Config:
        env_prefix = "PG_"
        env_file = ".env"