from practise.DB_ORM_migration.orm.db_shop.models import (
    Base,
    Session,
    Customer,
    Cart,
    Product,
    ProductPhoto
)
from practise.DB_ORM_migration import fake_customer, fake_customer_2, generate_products


def add_customers(count):
    session = Session()

    # session.add_all([item1, item2, item3])
    #session.add_all([Customer(**fake_customer_2(cust)id)) for _ in range(1, count+1)])

    customers = []
    for _ in range(1, count + 1):
        fake_cust = fake_customer()
        cust = Customer(name=fake_cust['name'],
                                  phone=fake_cust['phone'],
                                  email=fake_cust['email']
                                  )
        print(cust)
    #
    #     customers.append(Customer(name=cust['name'],
    #                               phone=cust['phone'],
    #                               email=cust['email']
    #                               ))
    #
    #
    # session.add_all(customers)
    # session.commit()
    #
    # print(customers)

    session.close()


def add_product():
    pass


def main():
    add_customers(5)


if __name__ == '__main__':
    main()
