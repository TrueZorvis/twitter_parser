from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from twitter_parser.database import Base


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, index=True)

    users = relationship("User", back_populates="session")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))
    status = Column(String(255))
    session_id = Column(Integer, ForeignKey("sessions.session_id", ondelete="CASCADE"))

    session = relationship("Session", back_populates="users")
    user_data = relationship("UserData", back_populates="users")


class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True)
    twitter_id = Column(Integer, unique=True)
    name = Column(String(255))
    username = Column(String(255), unique=True)
    following_count = Column(Integer)
    followers_count = Column(Integer)
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    users = relationship("User", back_populates="user_data")
    user_tweets = relationship("UserTweet", back_populates="user_data")


class UserTweet(Base):
    __tablename__ = "user_tweets"

    id = Column(Integer, primary_key=True)
    tweet = Column(String)
    twitter_id = Column(Integer, ForeignKey("user_data.twitter_id", ondelete="CASCADE"))

    user_data = relationship("UserData", back_populates="user_tweets")
