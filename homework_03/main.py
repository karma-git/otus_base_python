"""
Домашнее задание №3
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""
import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from homework_03.models import engine, Base, Session, User, Post
from sqlalchemy.ext.asyncio import AsyncSession
from homework_03.jsonplaceholder_requests import receive_api_data


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_to_db(rows: list):
    async with Session() as session:
        session: AsyncSession

        async with session.begin():
            session.add_all(rows)

        await session.commit()


def json_to_user_model(user: dict) -> User:
    u = User(id=user['id'],
             name=user['name'],
             username=user['username'],
             email=user['email'])
    return u


def json_to_post_model(post: dict) -> Post:
    p = Post(title=post['title'],
             body=post['body'],
             user_id=post['userId'])
    return p


async def fetch_users_with_posts():
    async with Session() as session:
        session: AsyncSession

        statement = select(User).options(selectinload(User.posts))

        result = await session.execute(statement)
        print(f"users: {result}")  # users: <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x106cb91f0>

        for user in result.scalars():
            print(user)
            print(user.posts)


async def async_main():
    await create_tables()
    raw_users, raw_posts = await receive_api_data()
    users = [json_to_user_model(user) for user in raw_users]
    posts = [json_to_post_model(post) for post in raw_posts]
    await add_to_db(users)
    await add_to_db(posts)
    await fetch_users_with_posts()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
