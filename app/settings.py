from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    MAIN_SERVICE_URL: str = os.environ.get('MAIN_SERVICE_URL')
    AUTH_SERVICE_URL: str = os.environ.get('AUTH_SERVICE_URL')
    GATEWAY_TIMEOUT: int = 59


settings = Settings()
