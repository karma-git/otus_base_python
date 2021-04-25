from sqlalchemy import (
    Column,
    Integer,
    String
)

from practise.DB_ORM_migration.orm.db_shop.models import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r}, email={self.email})"

    def __repr__(self):
        return str(self)

