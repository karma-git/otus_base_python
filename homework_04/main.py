"""
Домашнее задание №4
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
import os

from sqlalchemy import select, func, join
from sqlalchemy.orm import selectinload

from models import engine, Base, Session, User, Post
from sqlalchemy.ext.asyncio import AsyncSession
from jsonplaceholder_requests import receive_api_data


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
    u = User(
        id=user["id"], name=user["name"], username=user["username"], email=user["email"]
    )
    return u


def json_to_post_model(post: dict) -> Post:
    p = Post(title=post["title"], body=post["body"], user_id=post["userId"])
    return p


async def fetch_users_with_posts():
    async with Session() as session:
        session: AsyncSession

        statement = select(User).options(selectinload(User.posts))

        result = await session.execute(statement)
        print(
            f"users: {result}"
        )  # users: <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x106cb91f0>

        for user in result.scalars():
            print(user)
            print(user.posts)


async def fetch_users_posts_count():
    async with Session() as session:
        session: AsyncSession

        # calculate posts which assigned to user
        # select u.username, count(p.user_id) from users u left join posts p on p.user_id=u.id group by u.username;
        user_posts_count = func.count(Post.user_id).label("total_posts")
        j = join(User, Post, User.id == Post.user_id)
        stmt = (
            select(User.username, User.email, user_posts_count)
            .select_from(j)
            .group_by(User.username, User.email)
            .order_by(User.username)
        )

        result = await session.execute(stmt)
        for user in result:
            print(user)


async def async_main():
    await create_tables()
    raw_users, raw_posts = await receive_api_data()
    users = [json_to_user_model(user) for user in raw_users]
    posts = [json_to_post_model(post) for post in raw_posts]
    await add_to_db(users)
    await add_to_db(posts)

    # queries
    await asyncio.gather(fetch_users_with_posts(), fetch_users_posts_count())


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    print(os.environ['SQLALCHEMY_PG_CONN_URI'])
    main()
