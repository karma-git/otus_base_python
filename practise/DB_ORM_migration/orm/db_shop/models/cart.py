from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship

from practise.DB_ORM_migration.orm.db_shop.models import Base
from practise.DB_ORM_migration.orm.db_shop.models.cart_product import CartProduct


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)

    products = relationship(
        "Product",
        secondary="cart_product",
        back_populates="cart"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, customer.id={self.customer_id})"

    def __repr__(self):
        return str(self)



