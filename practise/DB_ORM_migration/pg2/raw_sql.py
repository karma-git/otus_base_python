import psycopg2
from practise.DB_ORM_migration import (
    CONNECTION_VAGRANT_DB_SHOP,
    fake_customer,
    fake_product,
    generate_products
)
from random import randint


class DataBaseWorker:
    # conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)
    #
    # # some actions
    # cur = conn.cursor()
    # cur.execute()
    # cur.fetchall()
    #
    # conn.commit()
    # conn.close()

    def create_tables(self):
        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE customer (
                id SERIAl PRIMARY KEY,
                name VARCHAR(255),
                phone VARCHAR(20),
                email VARCHAR(255) UNIQUE NOT NULL
            );
            
            CREATE TABLE product (
                id SERIAl PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                description TEXT,
                price FLOAT
            );
            
            CREATE TABLE product_photo (
                id SERIAl PRIMARY KEY,
                url VARCHAR(255),
                /* ONE TO ONE connection between product and its photo */
                product_id INTEGER references product(id)
            );
            
            CREATE TABLE cart (
                id SERIAl PRIMARY KEY,
                /* ref between cart and its end customer */
                customer_id INTEGER references customer(id)
            );
            
            -- junction table for many-to-many  
            CREATE TABLE cart_product (
                cart_id integer references customer(id),
                product_id integer references product(id)
            );           
            """
        )
        conn.commit()
        conn.close()

    def add_customer(self, count):
        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)
        # some actions
        cur = conn.cursor()

        # add customer

        for i in range(count):
            cust = fake_customer()
            cur.execute(
                """                
                INSERT INTO customer (name, phone, email)
                VALUES (%s, %s, %s);  
                """, (cust['name'],
                      cust['phone'],
                      cust['email'])
            )

        conn.commit()
        conn.close()

    def add_product(self):
        products: list = generate_products()
        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)
        cur = conn.cursor()

        for product in products:
            # product
            cur.execute(
                """
                INSERT INTO product (name, description, price)
                VALUES (%s, %s, %s);
                """, (
                    product['name'],
                    product['description'],
                    product['price']
                )
            )

        conn.commit()

        for product in products:
            cur.execute(
                """
                INSERT INTO product_photo (url)
                VALUES (%s);
                """, [
                    product['photo_url']
                ]
            )

        conn.commit()

        conn.close()

    def fetch_customers(self):
        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)
        # some actions
        cur = conn.cursor()
        cur.execute("SELECT * FROM customer;")
        cust = cur.fetchall()
        #print(f"Length of select all <{len(cust)}>\n{cust}")

        for customer in cust:
            print(f"Customer => (name={customer[1]}, email={customer[3]}")

        conn.commit()
        conn.close()

    def fetch_products(self):
        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)
        # some actions
        cur = conn.cursor()
        cur.execute("SELECT * FROM product;")
        prod = cur.fetchall()

        for product in prod:
            print(f"Product => (name={product[1]}, price={product[3]} RUB)")

        conn.commit()
        conn.close()


def main():
    worker = DataBaseWorker()
    # worker.create_tables()

    # worker.add_customer(6)
    # worker.add_product()
    #worker.fetch_customers()
    worker.fetch_products()


if __name__ == '__main__':
    main()
