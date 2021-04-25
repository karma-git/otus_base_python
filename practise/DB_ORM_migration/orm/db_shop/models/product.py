from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Text
)

from practise.DB_ORM_migration.orm.db_shop.models import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r}, price={self.price!r})"

    def __repr__(self):
        return str(self)

