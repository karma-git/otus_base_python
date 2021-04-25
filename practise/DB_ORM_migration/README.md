# Цель:

Попрактиковаться с занятиями:
- 12 Хранение данных
- 13 ORM: SQLAlchemy. Связи в БД
- 14 Миграции: alembic, сложные связи в БД

* Научиться инсталировать БД (postgres / sqlite) в ОС / docker. 
* Попрактиковаться SQL.
* Практика с ORM.

# Описание:

Проект БД магазина, [вдохновлено](https://www.youtube.com/watch?v=WpojDncIWOw):   

# Installation options:
- Docker Copmpose
- soon: Vagrant + Ansible 

## Docker Compose
Fastest and easiest option:
### Clone repo
`git clone` # and enter the root folder
### Create env files
`touch hpostgres.env; dev.env;`
*postgres.env*
```
POSTGRES_USER=secretuser
POSTGRES_PASSWORD=secretpw
POSTGRES_DB=dbname
```
*dev.env*
```
host=secret_private_network
port=secret_port
database=dbname
user=secretuser
password=secretpw
```
### Install EnvFile plugin into PyCharm
Go to Preferences(osX) -> Plugins -> install EnvFile and follow the [manual](https://plugins.jetbrains.com/plugin/7861-envfile) to load dev.env
### Run docker
`$ docker compose up -d`
# Launch
Now you can run the main.py script (orm) via pycharm run
_____
## PG DUMP
- с сервера: `postgres@ubuntu-hirsute:/tmp$ pg_dump shop > shop.bac`
- с локальной машины: `$ pg_dump -h 192.168.1.6 shop -U postgres > shop.bac`
## Truncate
Чтобы почистить криво-заполненую табличку, можно сделать truncate и смыть id-шники. (вместо того чтобы лезть в pg и дропать базу).

`DataBase tools -> Truncate`