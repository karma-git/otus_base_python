from practise.DB_ORM_migration.orm.db_shop.models import (
    Base,
    Session,
    Customer,
    Cart,
    Product,
    ProductPhoto
)
from practise.DB_ORM_migration import fake_customer, generate_products


def add_customers(count):
    session = Session()

    # session.add_all([item1, item2, item3])
    session.add_all([Customer(**fake_customer()) for _ in range(1, count+1)])
    session.commit()

    session.close()


def add_product():
    session = Session()
    products: list = generate_products()
    prods, prod_ph = [], []

    for id, product in enumerate(products):
        id += 1  # offset for id
        url = product.pop('photo_url')
        prods.append(Product(**product))
        prod_ph.append(ProductPhoto(url=url, product_id=id))
    

    session.add_all(prods)
    session.add_all(prod_ph)
    session.commit()

    session.close()


def main():
    add_customers(6)
    add_product()


if __name__ == '__main__':
    main()
