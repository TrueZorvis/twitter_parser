"""
Конфигурация
"""
from pydantic import BaseSettings


class Settings(BaseSettings):

    API_PREFIX: str = '/api'
    DOCS_URL: str = '/'
    OPENAPI_URL: str = '/openapi.json'
    REDOC_URL: str = '/redoc'

    API_KEY: str = ''
    API_SECRET_KEY: str = ''
    API_BEARER_TOKEN: str = ''
    API_ACCESS_TOKEN: str = ''
    API_ACCESS_TOKEN_SECRET: str = ''


settings = Settings()
