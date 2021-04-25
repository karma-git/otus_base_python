from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from practise.DB_ORM_migration.orm.db_shop.config import DATABASE_URI

engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# print(f"тип => {type(session_factory)}, объект => {session_factory}\nнэймскоуп_словарь => {dir(session_factory)}", end=5*'\n')
# print(f"тип => {type(Session)}, объект => {Session}\nнэймскоуп_словарь => {dir(Session)}")


