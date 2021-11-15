import secrets
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Simple finance tracker"
    K_SERVICE: str = "Local"
    K_REVISION: str = "local"
    LOG_LEVEL: str = "DEBUG"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    FIRESTORE_EMULATOR_HOST: str = None


    class Config:
        env_file = ".env"


settings = Settings()
