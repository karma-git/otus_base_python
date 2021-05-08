"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
---
Забираем данные из API и превращаем в dataclass, возвращаем два списка - юзеры и посты
"""
import asyncio
from aiohttp import ClientSession
from dataclasses import dataclass

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


@dataclass
class User:
    name: str
    username: str
    email: str


@dataclass
class Post:
    title: str
    body: str


async def get_json(url: str) -> dict:
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def receive_api_data() -> tuple:
    get_users = asyncio.create_task(get_json(url=USERS_DATA_URL))
    get_posts = asyncio.create_task(get_json(url=POSTS_DATA_URL))
    raw_users = await get_users
    raw_posts = await get_posts

    users = [User(name=user['name'],
                  username=user['username'],
                  email=user['email'])
             for user in raw_users]

    posts = [Post(title=post['title'],
                  body=post['body'])
             for post in raw_posts]

    return users, posts


# TODO: import that to other module, delete debug
def main():
    result = asyncio.run(receive_api_data())
    print(result)


if __name__ == "__main__":
    main()
