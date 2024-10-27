DROP DATABASE IF EXISTS freshHarvest;
CREATE DATABASE freshHarvest;

USE freshHarvest;

CREATE TABLE person (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE staff (
    id INT PRIMARY KEY,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    dept_name VARCHAR(100),
    FOREIGN KEY (id) REFERENCES person (id)
);

CREATE TABLE customers (
    id INT PRIMARY KEY,
    address VARCHAR(200),
    balance FLOAT DEFAULT 0.0,
    max_owing FLOAT DEFAULT 100.0,
    FOREIGN KEY (id) REFERENCES person (id)
);

CREATE TABLE corporate_customers (
    id INT PRIMARY KEY,
    discount_rate FLOAT DEFAULT 0.1,
    credit_limit FLOAT,
    min_balance FLOAT DEFAULT 0.0,
    FOREIGN KEY (id) REFERENCES customers (id)
);

CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    amount FLOAT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

CREATE TABLE credit_card_payments (
    id INT PRIMARY KEY,
    card_number VARCHAR(16) NOT NULL,
    card_type VARCHAR(20),
    expiry_date VARCHAR(5),
    FOREIGN KEY (id) REFERENCES payments (id)
);

CREATE TABLE debit_card_payments (
    id INT PRIMARY KEY,
    bank_name VARCHAR(100),
    card_number VARCHAR(16),
    FOREIGN KEY (id) REFERENCES payments (id)
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    staff_id INT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES customers (id),
    FOREIGN KEY (staff_id) REFERENCES staff (id)
);

CREATE TABLE items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE veggies (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES items (id)
);

CREATE TABLE weighted_veggies (
    id INT PRIMARY KEY,
    weight FLOAT,
    price_per_kilo FLOAT,
    FOREIGN KEY (id) REFERENCES veggies (id)
);

CREATE TABLE pack_veggies (
    id INT PRIMARY KEY,
    num_of_pack INT,
    price_per_pack FLOAT,
    FOREIGN KEY (id) REFERENCES veggies (id)
);

CREATE TABLE unit_price_veggies (
    id INT PRIMARY KEY,
    price_per_unit FLOAT,
    quantity INT,
    FOREIGN KEY (id) REFERENCES veggies (id)
);

CREATE TABLE premade_boxes (
    id INT PRIMARY KEY,
    size VARCHAR(10),
    num_of_boxes INT,
    price FLOAT,
    FOREIGN KEY (id) REFERENCES items (id)
);

CREATE TABLE box_contents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    box_id INT,
    veggie_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (box_id) REFERENCES premade_boxes (id),
    FOREIGN KEY (veggie_id) REFERENCES veggies (id)
);

CREATE TABLE order_lines (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    item_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (item_id) REFERENCES items (id)
);



INSERT INTO person (first_name, last_name, password, username) 
VALUES 

('John', 'Doe', '872c4a0c7b4fce4bd95f6d52ce150c0a0cbe08d3d0d130b34c80af553c27cc0b', 'johndoe'),  
('Jane', 'Smith', '872c4a0c7b4fce4bd95f6d52ce150c0a0cbe08d3d0d130b34c80af553c27cc0b', 'janesmith'),  


('Alice', 'Johnson', '872c4a0c7b4fce4bd95f6d52ce150c0a0cbe08d3d0d130b34c80af553c27cc0b', 'alicejohnson'),  
('Bob', 'Brown', '872c4a0c7b4fce4bd95f6d52ce150c0a0cbe08d3d0d130b34c80af553c27cc0b', 'bobbrown');  


INSERT INTO staff (id, date_joined, dept_name) 
VALUES 
(1, CURRENT_TIMESTAMP, 'Sales'),  
(2, CURRENT_TIMESTAMP, 'Operations');  


INSERT INTO customers (id, address, balance, max_owing) 
VALUES 
(3, '123 Elm Street', 50.0, 100.0),  
(4, '456 Oak Avenue', 20.0, 100.0);  


INSERT INTO corporate_customers (id, discount_rate, credit_limit, min_balance) 
VALUES 
(4, 0.10, 5000.0, 100.0);  


-- Inserting data into payments table
INSERT INTO payments (amount, customer_id) 
VALUES 
(25.0, 3),  
(15.0, 4);

-- Inserting data into credit_card_payments table
INSERT INTO credit_card_payments (id, card_number, card_type, expiry_date) 
VALUES 
(1, '1234567812345678', 'Visa', '12/25'),  
(2, '8765432187654321', 'MasterCard', '01/26');

-- Inserting data into debit_card_payments table
INSERT INTO debit_card_payments (id, bank_name, card_number) 
VALUES 
(1, 'Bank of America', '1122334455667788'),  
(2, 'Chase', '9988776655443322');

-- Inserting data into orders table
INSERT INTO orders (customer_id, staff_id) 
VALUES 
(3, 1),  
(4, 2);


-- Inserting data into items table
INSERT INTO items (name) 
VALUES 
('Carrot'),  
('Tomato'),  
('Potato'),  
('Cucumber'),  
('Lettuce'),  
('Onion');

-- Inserting data into veggies table
INSERT INTO veggies (id) 
VALUES 
(1),  
(2),  
(3),  
(4),  
(5),  
(6);

-- Inserting data into weighted_veggies table
INSERT INTO weighted_veggies (id, weight, price_per_kilo) 
VALUES 
(1, 1.5, 3.0),  
(2, 2.0, 2.5),  
(3, 1.2, 4.0),  
(4, 1.0, 3.5),  
(5, 0.5, 5.0),  
(6, 2.5, 2.0);

-- Inserting data into pack_veggies table
INSERT INTO pack_veggies (id, num_of_pack, price_per_pack) 
VALUES 
(1, 10, 20.0),  
(2, 15, 30.0),  
(3, 20, 25.0),  
(4, 5, 15.0),  
(5, 12, 40.0),  
(6, 8, 35.0);

-- Inserting data into unit_price_veggies table
INSERT INTO unit_price_veggies (id, price_per_unit, quantity) 
VALUES 
(1, 2.0, 10),  
(2, 1.5, 20),  
(3, 3.0, 15),  
(4, 2.5, 25),  
(5, 4.0, 5),  
(6, 1.0, 30);

-- Inserting data into premade_boxes table
INSERT INTO premade_boxes (id, size, num_of_boxes, price) 
VALUES 
(1, 'Small', 5, 50.0),  
(2, 'Medium', 10, 100.0),  
(3, 'Large', 15, 150.0);

-- Inserting data into box_contents table
INSERT INTO box_contents (box_id, veggie_id, quantity) 
VALUES 
(1, 1, 3),  
(1, 2, 2),  
(2, 3, 5),  
(2, 4, 3),  
(3, 5, 10),  
(3, 6, 4);

-- Inserting data into order_lines table
INSERT INTO order_lines (order_id, item_id, quantity) 
VALUES 
(1, 1, 2),  
(1, 2, 1),  
(2, 3, 3),  
(2, 4, 2),  
(1, 5, 1),  
(2, 6, 1);
