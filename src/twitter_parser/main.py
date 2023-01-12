"""
Главный файл
"""
import uvicorn
from . import create_app
from .core import models
from twitter_parser.database import async_engine

app = create_app()


@app.on_event("startup")
async def db_setup():
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


if __name__ == '__main__':

    # Run the service
    uvicorn.run(
        '__main__:app',
        host="127.0.0.1",
        port=8000,
        log_level='debug',
        use_colors=False,
    )
