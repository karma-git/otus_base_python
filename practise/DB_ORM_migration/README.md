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

## PG DUMP
- с сервера: `postgres@ubuntu-hirsute:/tmp$ pg_dump shop > shop.bac`
- с локальной машины: `$ pg_dump -h 192.168.1.6 shop -U postgres > shop.bac`
## Truncate
Чтобы почистить криво-заполненую табличку, можно сделать truncate и смыть id-шники. (вместо того чтобы лезть в pg и дропать базу).

`DataBase tools -> Truncate`