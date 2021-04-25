from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship

from practise.DB_ORM_migration.orm.db_shop.models import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)

    customer = relationship("Customer", back_populates="cart")

    # tags = relationship(
    #     "Tag",
    #     secondary=posts_tags_table,
    #     back_populates="posts"
    # )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, customer.id={self.customer_id})"

    def __repr__(self):
        return str(self)



