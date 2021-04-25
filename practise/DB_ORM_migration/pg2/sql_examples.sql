--1) LEFT JOIN (21:23)
SELECT pp.*,p.name,p.price FROM product_photo pp
LEFT JOIN product p
ON p.id=pp.product_id;

-- GET customers with their sum of their average currency;
-- shop=# SELECT c.name, cart.id from customer c left join cart on cart.customer_id=c.id;
-- SELECT <поля  из всех сджойненных таблиц> from <table(первая таблица)> t(алиас для первой таблицы)
-- LEFT JOIN <table(подтягиваем след таблицу)> t
-- ON <подтянутая таблица>.<column со связью к основной таблице>=<предыдущая таблица>.<column предыдущей таблицы связанный с column сджойненной>
-- shop=# SELECT c.name,p.name,p.price,pp.url from customer c left join cart on cart.customer_id=c.id left join cart_product cp on cp.cart_id=cart.id left join product p on p.id=cp.product_id left join product_photo pp on pp.product_id=p.id WHERE (c.name iLIKE '%светлана%' OR c.name iLIKE '%маргар%');

--2) Выведем все покупки девушек, цена по убыванию
SELECT c.name,p.price,p.name,pp.url from customer c
    LEFT JOIN cart
    ON cart.customer_id=c.id

    LEFT JOIN cart_product cp
    ON cp.cart_id=cart.id

    LEFT JOIN product p
    ON p.id=cp.product_id

    LEFT JOIN product_photo pp
    ON pp.product_id=p.id

    WHERE (
        c.name iLIKE '%свет%'
            OR
        c.name iLIKE '%марг%')
    ORDER BY p.price DESC;

--3) Вывести сумму корзины по всем покупателям
SELECT c.name,
       SUM(p.price)
       from customer c

    LEFT JOIN cart
    ON cart.customer_id=c.id

    LEFT JOIN cart_product cp
    ON cp.cart_id=cart.id

    LEFT JOIN product p
    ON p.id=cp.product_id

    GROUP BY c.name

    ORDER BY sum DESC;

--4) Вывести покупателей и сумму  корзины, если она больше 180к (HAVING фильтрует именно группы (которые GROUP BY) (WHERE - конкретные строки))
SELECT c.name,
       SUM(p.price)
       from customer c

    LEFT JOIN cart
    ON cart.customer_id=c.id

    LEFT JOIN cart_product cp
    ON cp.cart_id=cart.id

    LEFT JOIN product p
    ON p.id=cp.product_id

    GROUP BY c.name

    HAVING sum(p.price)>180000;

--5) Limit + offset
SELECT c.name,p.name,p.price,pp.url from customer c
    left join cart
    on cart.customer_id=c.id

    left join cart_product cp
    on cp.cart_id=cart.id

    left join product p
    on p.id=cp.product_id

    left join product_photo pp
    on pp.product_id=p.id
    limit 7
    offset 2;















 


