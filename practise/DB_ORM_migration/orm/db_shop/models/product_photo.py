from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from practise.DB_ORM_migration.orm.db_shop.models import Base


class ProductPhoto(Base):
    __tablename__ = "product_photo"

    id = Column(Integer, primary_key=True)
    url = Column(String(255), unique=True)

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)

    #product = relationship("Product", back_populates="product_photo")
    product = Column(Integer, ForeignKey("product.id"), nullable=False)

    # tags = relationship(
    #     "Tag",
    #     secondary=posts_tags_table,
    #     back_populates="posts"
    # )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, product.id={self.product_id})\n" \
               f"Product Photo Link => {self.url}"

    def __repr__(self):
        return str(self)



