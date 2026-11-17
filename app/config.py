# TODO: DB settings and secrets loaded from .env
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_host: str
    db_port: int = 3306
    db_user: str
    db_password: str
    db_name: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()