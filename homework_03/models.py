"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import os
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

#PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://postgres:password@localhost/postgres"
PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://postgres:secretpassword@localhost/postgres"


engine = create_async_engine(PG_CONN_URI)

Base = declarative_base()

Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)

    posts = relationship("Post", back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, " \
               f"username={self.username}, email={self.email})"

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    body = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="posts")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title}, " \
               f"user_id={self.user_id})"

    def __repr__(self):
        return str(self)










