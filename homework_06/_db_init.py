#!/usr/bin/python3
import psycopg2
import os
from config import CONN

CONN['host']=os.environ.get('DB_HOST', '0.0.0.0')

def main():
    try:
        conn = psycopg2.connect(**CONN)
    except Exception as e:
        pass
    else:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                    WHERE table_catalog='shop' AND
                     table_schema='public' AND
                      table_name='product'
            );
            """
        )
        is_table_exists = cur.fetchone()[0]
        if not is_table_exists:
            cur.execute(
                """
                CREATE TABLE product (
                    id SERIAl PRIMARY KEY,
                    goods VARCHAR(255) UNIQUE NOT NULL,
                    description TEXT,
                    price FLOAT
                );
                """
            )
            conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
