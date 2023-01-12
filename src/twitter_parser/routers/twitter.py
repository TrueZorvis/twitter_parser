"""
Реализация REST
"""
from fastapi import APIRouter, Path, Depends, BackgroundTasks
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from twitter_parser.dependencies import get_async_session
from twitter_parser.core.adapter import TwitterAdapter
from twitter_parser.config import settings

router = APIRouter(tags=['twitter'],)
twitter = TwitterAdapter(
    settings.API_KEY,
    settings.API_SECRET_KEY,
    settings.API_BEARER_TOKEN,
    settings.API_ACCESS_TOKEN,
    settings.API_ACCESS_TOKEN_SECRET,
)


@router.post(
    "/users",
)
async def parse_users(
        urls: List[str],
        background_tasks: BackgroundTasks,
        async_session: AsyncSession = Depends(get_async_session)
):
    new_session = await twitter.parse_users(
        urls=urls,
        async_session=async_session,
        bg_tasks=background_tasks
    )
    return new_session


@router.get(
    "/users/status/{session_id}",
)
async def get_parse_status(
        session_id: int = Path(..., title='ID сессии', description='ID сессии', example='42'),
        async_session: AsyncSession = Depends(get_async_session)
):
    status = await twitter.get_parse_status(
        session_id=session_id,
        async_session=async_session
    )
    return status


@router.get(
    "/user/{username}",
)
async def get_user_data(
        username: str = Path(..., title='Твиттер аккаунт', description='Твиттер аккаунт', example='elonmusk'),
        async_session: AsyncSession = Depends(get_async_session)
):
    return await twitter.get_user_data(
        username=username,
        async_session=async_session
    )


@router.get(
    "/tweets/{twitter_id}",
)
async def get_user_tweets(
        twitter_id: int = Path(..., title='ID твиттер аккаунта', description='ID твиттер аккаунта', example=42),
        async_session: AsyncSession = Depends(get_async_session)
):
    return await twitter.get_user_tweets(
        twitter_id=twitter_id,
        async_session=async_session
    )
