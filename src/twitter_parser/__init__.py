"""
Инициализация
"""
from fastapi import FastAPI

from .routers import twitter
from .config import settings


__title__ = 'Twitter Parser'
__version__ = '0.1.0'


def create_app() -> FastAPI:
    """Проинициализировать FastAPI-приложение.

    Returns:
        app: FastAPI application
    """

    app = FastAPI(
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        openapi_url=settings.OPENAPI_URL,
        title=__title__,
        description="Парсер твиттера",
        version=__version__,
        )

    app.include_router(twitter.router, prefix=settings.API_PREFIX)

    return app
