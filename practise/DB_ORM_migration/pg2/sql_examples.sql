-- 1) Create new database
CREATE DATABASE shop;

-- Connect to new db  in psql via `$ \c shop` or `psql -h 192.168.1.X shop -U postgres`

-- 2) Create tables
CREATE TABLE customer (
    id SERIAl PRIMARY KEY,
    name VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255)
);

CREATE TABLE product (
    id SERIAl PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price FLOAT
);


 


