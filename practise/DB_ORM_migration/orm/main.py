from random import randint, choice, sample, choices

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
    session.add_all([Customer(**fake_customer()) for _ in range(1, count + 1)])
    session.commit()
    session.close()

    session.add_all([Cart(customer_id=i) for i in range(1, count + 1)])
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
    session.commit()

    session.add_all(prod_ph)
    session.commit()

    session.close()


def add_cart_product():
    session = Session()
    carts = session.query(Cart).all()

    # Let's add random quantity of goods for each customer's cart
    cust: Cart
    for cust in carts:
        # Нужно для его cust.products.append(Product(id))
        products = session.query(Product).all()
        random_counts = randint(1, len(products))
        random_products = sample(products, k=random_counts)
        for prod in random_products:
            cust.products.append(prod)

    session.commit()
    session.close()


def deploy_db(cust_count: int):
    add_customers(cust_count)
    add_product()
    add_cart_product()


def select():
    session = Session()
    cust = session.query(Customer).all()
    print(type(cust), cust)


def main():
    # deploy_db(6)
    select()


if __name__ == '__main__':
    main()
