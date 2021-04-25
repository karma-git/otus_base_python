# Let's prepare an ORM driven project
Catalog structure:
```
$ tree                            
.
├── __init__.py
├── __pycache__
│   └── __init__.cpython-39.pyc
├── db_shop
│   ├── __init__.py
│   ├── config.py
│   └── models
│       ├── __init__.py
│       ├── base.py
│       └── customer.py
└── orm_readme.md
```
Base.py
==
### create engine
```
from sqlalchemy import create_engine
...
from <some_package> import config.DB_URI

engine = create_engine(DB_URI, echo=True)  # echo true - show sql statements
```

`DB_URI = "postgresql://postgres:superstrongpassword@127.0.0.1:5432/postgres"`

Since sqlAlch 1.4 we should use driver name ***postgresql*** instead of ***postgres***.

URI format : `"<driver>://<user>:<password>@<host>/<db>"`
### declarative_base
```
...
from sqlalchemy.ext.declarative import declarative_base
...
Base = declarative_base(bind=engine)
```
What is [Base](https://stackoverflow.com/questions/15175339/sqlalchemy-what-is-declarative-base)? [Documentation](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html)

declarative_base() is a factory function that constructs a base class for declarative class definitions (which is assigned to the Base variable in your example). The one you created in user.py is associated with the User model, while the other one (in main.py) is a different class and doesn't know anything about your models, that's why the Base.metadata.create_all() call didn't create the table. You need to import Base from user.py
### session
```
...
from sqlalchemy.orm import sessionmaker, scoped_session
...
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
```
What is session / [scoped session](https://docs.sqlalchemy.org/en/14/orm/contextual.html?highlight=scoped)?

предусмотрена функция scoped_session() , которая создает управляемый потоком реестр объектов Session . Он обычно используется в веб-приложениях, так что одна глобальная переменная может использоваться для безопасного представления транзакционных сеансов с наборами объектов, локализованных в одном потоке.


Короче говоря, используйте scoped_session() для обеспечения безопасности резьбы.

SQLAlchemy includes its own helper object, which helps with the establishment of user-defined Session scopes. It is also used by third-party integration systems to help construct their integration schemes.

The object is the scoped_session object, and it represents a registry of Session objects. If you’re not familiar with the registry pattern, a good introduction can be found in [Patterns of Enterprise Architecture](https://martinfowler.com/eaaCatalog/registry.html).
```

print(f"тип => {type(session_factory)}, объект => {session_factory}\nнэймскоуп_словарь => {dir(session_factory)}", end=5*'\n')
print(f"тип => {type(Session)}, объект => {Session}\nнэймскоуп_словарь => {dir(Session)}")


тип => <class 'sqlalchemy.orm.session.sessionmaker'>, объект => sessionmaker(class_='Session', bind=Engine(postgresql://postgres:***@192.168.1.6:5432/shop), autoflush=True, autocommit=False, expire_on_commit=True)
нэймскоуп_словарь => ['__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'begin', 'class_', 'close_all', 'configure', 'identity_key', 'kw', 'object_session']




тип => <class 'sqlalchemy.orm.scoping.scoped_session'>, объект => <sqlalchemy.orm.scoping.scoped_session object at 0x103a37a30>
нэймскоуп_словарь => ['__call__', '__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_proxied', 'add', 'add_all', 'autocommit', 'autoflush', 'begin', 'begin_nested', 'bind', 'bulk_insert_mappings', 'bulk_save_objects', 'bulk_update_mappings', 'close', 'close_all', 'commit', 'configure', 'connection', 'delete', 'deleted', 'dirty', 'execute', 'expire', 'expire_all', 'expunge', 'expunge_all', 'flush', 'get', 'get_bind', 'identity_key', 'identity_map', 'info', 'is_active', 'is_modified', 'merge', 'new', 'no_autoflush', 'object_session', 'query', 'query_property', 'refresh', 'registry', 'remove', 'rollback', 'scalar', 'session_factory']
```
## Models
Create your model. Don't forget to import Base into model and inherit from it
## moodels package
```
from practise.DB_ORM_migration.orm.db_shop.models.base import Base
from practise.DB_ORM_migration.orm.db_shop.models.customer import Customer
```
It's needs to be imported into models package for alembic
# Initialise alembic
```
$ pwd
/Users/ah/repos/otus/practise/DB_ORM_migration/orm

$ alembic init alembic
  Creating directory /Users/ah/repos/otus/practise/DB_ORM_migration/orm/alembic ...  done
  Creating directory /Users/ah/repos/otus/practise/DB_ORM_migration/orm/alembic/versions ...  done
  Generating /Users/ah/repos/otus/practise/DB_ORM_migration/orm/alembic/script.py.mako ...  done
  Generating /Users/ah/repos/otus/practise/DB_ORM_migration/orm/alembic/env.py ...  done
  Generating /Users/ah/repos/otus/practise/DB_ORM_migration/orm/alembic/README ...  done
  Generating /Users/ah/repos/otus/practise/DB_ORM_migration/orm/alembic.ini ...  done
  Please edit configuration/connection/logging settings in '/Users/ah/repos/otus/practise/DB_ORM_migration/orm/alembic.ini' before proceeding.
```
Now project folder should look like:
```
$ tree
.
├── __init__.py
├── __pycache__
│   └── __init__.cpython-39.pyc
├── alembic
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── alembic.ini
├── db_shop
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   └── config.cpython-39.pyc
│   ├── config.py
│   └── models
│       ├── __init__.py
│       ├── base.py
│       └── customer.py
└── orm_readme.md

6 directories, 14 files
```
Go to alembic -> env.py and import metada (lines 19+):
```
from practise.DB_ORM_migration.orm.db_shop.models import Base
target_metadata = Base.medata
```
Add DB_URI into alembic.ini -> sqlalchemy.url
Also you may need to correct syspath for alembic (for projects wit complicated folder schema), like me:
```
#prepend_sys_path = .
prepend_sys_path = /Users/ah/repos/otus
```
### Migrate
! Check migration after revision, and only after review perform upgrade 
```
(otus_venv) 
~/repos/otus/practise/DB_ORM_migration/orm on  develop! ⌚ 9:49:30
$ alembic revision --autogenerate -m "init migration"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'customer'
  Generating /Users/ah/repos/otus/practise/DB_ORM_migration/orm/alembic/versions/bb7e42472e18_init_migration.py ...  done
(otus_venv) 
~/repos/otus/practise/DB_ORM_migration/orm on  develop! ⌚ 9:49:39
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> bb7e42472e18, init migration
(otus_venv)
```
# Models, many-to-many:
- Апгрейд миграции с помощью alembic изменяет схему БД, без всяких Base.metadata.create_all().

revision - подготавливает файл миграции (конструирует sql запрос на основании измениний моделей),
  
upgrade head / hash - выкатывает миграцию (изменяет схему БД)
- Файлы миграций можно тупо удалять, но наверно нужно будет отодвинуть голову алембика (даунгрейд).

- Многие ко многим:

Есть нюанс с импортом и моделью для alembic. Не нужно импортировать модель в package models, модель нужно напрямую проимпортировать к тем моделям, которые создают связть многие ко многим.

Так же, если мы используем модель в виде class, а не переменной table =; то в зависимых моделях в secondary= - мы указываем не класс модели, а имя таблицы (str) -> "cart_product"
## add data to database via ORM
hi world form sql
## queries
