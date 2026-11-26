# DB settings and secrets loaded from .env
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_host: str
    db_port: int = 3306
    db_user: str
    db_password: str
    db_name: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_secconds: int = 30 * 24 * 60 * 60 # 30 days

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()