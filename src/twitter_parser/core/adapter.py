"""
Адаптер
"""
import tweepy
import time
from fastapi import BackgroundTasks
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from twitter_parser.core import models, schemas


class TwitterAdapter:
    def __init__(self, api_key, api_secret_key, api_bearer_token, api_access_token, api_access_token_secret):
        self.__bearer_token = api_bearer_token

        self.auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, api_access_token, api_access_token_secret)
        self.api = tweepy.API(self.auth)

    async def get_user_by_twitter_id(self, twitter_id: int, async_session: AsyncSession):
        result = await async_session.execute(
            select(models.UserData)
            .where(models.UserData.twitter_id == twitter_id))
        return result.scalars().first()

    async def get_user_id_by_session_id(self, url: str, session_id: int, async_session: AsyncSession):
        result = await async_session.execute(
            select(models.User)
            .where(models.User.url == url, models.User.session_id == session_id))
        return result.one()[0].id

    async def parse_all_urls(self, urls: List[str], session_id: int, async_session: AsyncSession):
        for url in urls:
            username = url.split('/')[-1]
            try:
                tw_user = self.api.get_user(screen_name=username)
                time.sleep(5)
                tweets_list = self.api.user_timeline(screen_name=username, count=10)
            except Exception:
                status = 'failed'
                print(f'Error while parsing twitter account {username}')
            else:
                status = 'success'
                print(f'Success while parsing twitter account {username}')

                existing_user = await self.get_user_by_twitter_id(tw_user.id, async_session)
                user_id = await self.get_user_id_by_session_id(url, session_id, async_session)
                if existing_user:
                    await async_session.execute(
                        update(models.UserData)
                        .values({
                            'name': tw_user.name,
                            'username': tw_user.screen_name,
                            'following_count': tw_user.friends_count,
                            'followers_count': tw_user.followers_count,
                            'description': tw_user.description,
                            'user_id': user_id
                        })
                        .filter(models.UserData.twitter_id == tw_user.id))
                    await async_session.commit()
                else:
                    async_session.add(models.UserData(
                        twitter_id=tw_user.id,
                        name=tw_user.name,
                        username=tw_user.screen_name,
                        following_count=tw_user.friends_count,
                        followers_count=tw_user.followers_count,
                        description=tw_user.description,
                        user_id=user_id
                    ))
                    await async_session.commit()

                new_tweets = []
                for tweet in tweets_list:
                    new_tweets.append(models.UserTweet(
                        tweet=tweet.text,
                        twitter_id=tw_user.id
                    ))
                async_session.add_all(new_tweets)
                await async_session.commit()

            finally:
                await async_session.execute(
                    update(models.User)
                    .values({'status': status})
                    .filter(models.User.url == url, models.User.session_id == session_id))
                await async_session.commit()
                time.sleep(5)

    async def parse_users(self, urls: List[str], async_session: AsyncSession, bg_tasks: BackgroundTasks):

        new_session = models.Session()
        async_session.add(new_session)
        await async_session.commit()

        new_users = []
        for url in urls:
            new_users.append(models.User(
                url=url,
                status='pending',
                session_id=new_session.session_id
            ))
        async_session.add_all(new_users)
        await async_session.commit()

        bg_tasks.add_task(self.parse_all_urls, urls, new_session.session_id, async_session)

        return new_session

    async def get_parse_status(self, session_id: int, async_session: AsyncSession):
        result = await async_session.execute(
            select(models.UserData.username, models.User.status)
            .join_from(models.UserData, models.User)
            .order_by(models.UserData.username)
            .filter(models.User.session_id == session_id)
        )
        return result.fetchall()

    async def get_user_data(self, username: str, async_session: AsyncSession) -> schemas.UserDataOut:
        result = await async_session.execute(
            select(models.UserData)
            .filter(models.UserData.username == username))

        try:
            result = result.one()[0]
        except Exception:
            return None
        else:
            return schemas.UserDataOut.parse_obj({
                'twitter_id': result.twitter_id,
                'name': result.name,
                'username': result.username,
                'following_count': result.following_count,
                'followers_count': result.followers_count,
                'description': result.description
            })

    async def get_user_tweets(self, twitter_id: int, async_session: AsyncSession):
        result = await async_session.execute(
            select(models.UserTweet)
            .filter(models.UserTweet.twitter_id == twitter_id)
            .order_by(models.UserTweet.id.desc())
            .limit(10)
        )
        result = result.scalars().all()
        return [res.tweet for res in result]
