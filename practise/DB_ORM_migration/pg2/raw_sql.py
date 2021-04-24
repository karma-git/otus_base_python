import psycopg2
from practise.DB_ORM_migration import (
    CONNECTION_VAGRANT_DB_SHOP,
    fake_customer,
    fake_product,
    generate_products
)
from random import randint, sample


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
                
                INSERT INTO product_photo (url)
                VALUES (%s);
                """, (
                    product['name'],
                    product['description'],
                    product['price'],
                    product['photo_url']
                )
            )

        conn.commit()

        conn.close()

    def insert_product_photo_id(self):
        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)

        # some actions
        cur = conn.cursor()

        product_count = self.calculate_products_count()

        for i in range(1, product_count + 1):
            cur.execute("""
                UPDATE product_photo
                SET product_id = (%s)
                WHERE id = (%s);
                """, (i, i)
            )

        conn.commit()
        conn.close()

    def insert_cart_id(self):
        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)

        # some actions
        cur = conn.cursor()
        customers_count = self.calculate_customers_count()

        for i in range(1, customers_count + 1):
            cur.execute(
                "INSERT INTO cart (customer_id)"
                "VALUES (%s);", [i]
            )

        conn.commit()
        conn.close()

    def random_products(self) -> tuple:
        products_count = randint(1, 6)
        rand_prod = lambda: sample([product_id for product_id in range(1, products_count + 1)], products_count)
        return rand_prod(), products_count

    def statement_formatter(self, cust_id: int, products: list, products_qty: int) -> tuple:
        result = ()
        for prod in products:
            result = (*result, cust_id, prod)

        return result

    def create_cart_product_relation(self):
        "Let's create 3 products in each customers cart"
        products_count = self.calculate_products_count()
        customers_count = self.calculate_customers_count()
        sql_statement = "INSERT INTO cart_product (cart_id, product_id) VALUES (%s, %s);"

        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)
        cur = conn.cursor()

        for cust in range(1, customers_count + 1):
            products: list
            products_count: int
            products, products_qty = self.random_products()

            statement = products_qty * sql_statement
            formatter = self.statement_formatter(cust, products, products_qty)

            cur.execute(statement, formatter)

        conn.commit()
        conn.close()

    def calculate_products_count(self) -> int:
        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)

        # some actions
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM product;")
        count = cur.fetchall()
        product_count = count[0][0]
        conn.close()
        return product_count

    def calculate_customers_count(self) -> int:
        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)

        # some actions
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM customer;")
        count = cur.fetchall()
        customer_count = count[0][0]
        conn.close()
        return customer_count

    def deploy_tables(self):
        # 1 create all tables
        self.create_tables()
        # 2 add customers, product
        self.add_customer(4)
        self.add_product()
        # 3 add prod_ph, cart
        self.insert_product_photo_id()
        self.insert_cart_id()
        # 4 add connection into junction table
        self.create_cart_product_relation()

    def fetch_customers(self):
        conn = psycopg2.connect(**CONNECTION_VAGRANT_DB_SHOP)
        # some actions
        cur = conn.cursor()
        cur.execute("SELECT * FROM customer;")
        cust = cur.fetchall()
        # print(f"Length of select all <{len(cust)}>\n{cust}")

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
    worker.deploy_tables()

    # QUERIES
    worker.fetch_customers()


if __name__ == '__main__':
    main()
