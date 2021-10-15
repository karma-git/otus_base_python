#!/usr/bin/python3
import os
import sys
from time import time, sleep
import psycopg2
from loguru import logger


def postgress_health_check(pg_config: dict, timeout: int):
    health_check_timeout = time() + timeout
    while True:

        if time() > health_check_timeout:
            logger.critical("Healthcheck didn't passed, exit 1")
            sys.exit(1)
            break

        try:
            conn = psycopg2.connect(**pg_config)
        except Exception as e:
            pass
        else:
            cur = conn.cursor()
            result = cur.execute("SELECT 1")
            logger.info("Looks like postgres is available, exiting -> {}", result)
            break
        finally:
            sleep(3)
            try:
                conn.close()
            except UnboundLocalError:
                pass


def payload(pg_config: dict):
    try:
        conn = psycopg2.connect(**pg_config)
        logger.debug("psycopg2 connect instance {}", conn)
    except Exception as e:
        logger.error(
            "Something is wrong with connect <cls={}>,<desc={}>", type(e).__name__, e
        )
    else:
        cur = conn.cursor()
        logger.debug("Connect to DB! -> cursor instance {}", cur)
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
        logger.debug("Select result -> {}", is_table_exists)
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
            logger.info("Table has been created has been completed")
    finally:
        try:
            conn.close()
        except Exception as e:
            logger.info(
                "Could not finalize conn <cls={}>,<desc={}>", type(e).__name__, e
            )


def main(logger_level: str):
    logger.remove(0)
    logger.add(sys.stderr, level=logger_level)
    try:
        CONNECTION = {
            "host": os.environ["host"],
            "port": os.environ["port"],
            "database": os.environ["database"],
            "user": os.environ["user"],
            "password": os.environ["password"],
            "connect_timeout": os.environ.get("connect_timeout", 2),
        }
    except KeyError as e:
        logger.critical(
            "One of env CONNECTION env vars is not set <cls={}>,<desc={}>",
            type(e).__name__,
            e,
        )
    else:
        postgress_health_check(CONNECTION, 60)
        logger.info("Healthcheck has been passed")
        payload(CONNECTION)
        logger.info("Program has been completed")


if __name__ == "__main__":
    main("INFO")
