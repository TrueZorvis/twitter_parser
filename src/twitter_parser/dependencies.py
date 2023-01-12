from twitter_parser.database import SessionLocal


# Dependency
async def get_async_session():
    async_session = SessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()
