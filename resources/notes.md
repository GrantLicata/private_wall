<---- Styling the Views ---->
Bootstrap Cheat Sheet:  https://getbootstrap.com/docs/5.2/examples/cheatsheet/

<---- Flask Installs @ Commands ---->
Install B-crypt:
    pipenv install flask-bcrypt

Remove GitHub connection:
     rm -rf .git

<---- Common SQL Queries ---->
Insert:
    INSERT INTO table_name (column_name1, column_name2) 
    VALUES('column1_value', 'column2_value');

Update/Edit:
    UPDATE table_name
    SET column1 = value1, column2 = value2, ...
    WHERE condition;

Delete:
    DELETE FROM table_name WHERE condition;

Join One to One:
    SELECT * FROM customers 
    JOIN addresses ON addresses.id = customers.address_id;

Join One to Many:
    SELECT * FROM orders 
    JOIN customers ON customers.id = orders.customer_id;

Join Many to Many:
    SELECT * FROM orders 
    JOIN items_orders ON orders.id = items_orders.order_id 
    JOIN items ON items.id = items_orders.item_id;