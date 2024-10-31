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
    customer_id INT NOT NULL,
    type ENUM('credit_card', 'debit_card') NOT NULL DEFAULT 'credit_card',  
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

CREATE TABLE credit_card_payments (
    id INT PRIMARY KEY,
    card_number VARCHAR(16) NOT NULL,
    card_type VARCHAR(20) NOT NULL,
    expiry_date VARCHAR(10) NOT NULL,
    type VARCHAR(20) NOT NULL DEFAULT 'credit_card',  
    FOREIGN KEY (id) REFERENCES payments (id)
);

CREATE TABLE debit_card_payments (
    id INT PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    card_number VARCHAR(16) NOT NULL,
    type VARCHAR(20) NOT NULL DEFAULT 'debit_card',
    FOREIGN KEY (id) REFERENCES payments (id)
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pending',
    total FLOAT DEFAULT 0.0,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

CREATE TABLE items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price FLOAT,  
    type ENUM('weighted_veggies', 'pack_veggies', 'unit_price_veggies', 'bunch_veggies','premade_box') NOT NULL
);

CREATE TABLE veggies (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES items (id)
);

CREATE TABLE weighted_veggies (
    id INT PRIMARY KEY,
    weight FLOAT,
    space_occupied FLOAT,
    FOREIGN KEY (id) REFERENCES veggies (id)
);

CREATE TABLE pack_veggies (
    id INT PRIMARY KEY,
    num_of_pack INT,
    space_occupied FLOAT,

    FOREIGN KEY (id) REFERENCES veggies (id)
);

CREATE TABLE unit_price_veggies (
    id INT PRIMARY KEY,
    space_occupied FLOAT,

    FOREIGN KEY (id) REFERENCES veggies (id)
);

CREATE TABLE bunch_veggies (
    id INT PRIMARY KEY,
    num_of_bunch INT,
    space_occupied FLOAT,
    FOREIGN KEY (id) REFERENCES veggies (id)
);

CREATE TABLE premade_boxes (
    id INT PRIMARY KEY,
    size VARCHAR(10),
    price FLOAT,
    space FLOAT,
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


INSERT INTO items (name, type,price) 
VALUES 

('Carrot','weighted_veggies',1.79),  
('Tomato','weighted_veggies',6.99),  
('Ginger','weighted_veggies',9.99),  
('Potato','weighted_veggies',2.79),  
('Onion','weighted_veggies',2.79),


('Lettuce', 'pack_veggies',2.49),  
('Garlic','pack_veggies',2.99),  
('Spinach','pack_veggies',4.99),  
('Bai Choy','pack_veggies',0.99),  


('pumpkin','unit_price_veggies', 4.49),  
('Capsicum','unit_price_veggies', 1.70),  
('Eggplant','unit_price_veggies', 1.99),  
('Cucumber','unit_price_veggies', 2.49),  
('Broccoli','unit_price_veggies',1.99),  
('Cauliflower','unit_price_veggies', 3.49), 
('Celery','unit_price_veggies',4.49),  

('Asparagus', 'bunch_veggies',5),  
('Leek','bunch_veggies', 2.99),  
('Spring Onion','bunch_veggies', 1.99),  
('Coriander','bunch_veggies', 1.49),


('Small Box', 'premade_box', 0.50),  
('Medium Box', 'premade_box', 1.00),  
('Large Box', 'premade_box', 1.50);  


INSERT INTO veggies (id) 
VALUES 
(1),  
(2),  
(3),  
(4),  
(5),  
(6),  
(7),  
(8),  
(9),  
(10),  
(11),  
(12),  
(13),  
(14),  
(15),  
(16),  
(17),  
(18),  
(19),  
(20);

INSERT INTO weighted_veggies (id, weight,space_occupied) 
VALUES 
(1, 1.0, 1.5),  
(2, 1.0, 1),  
(3, 1.0, 2),  
(4, 1.0, 1.5),  
(5, 1.0, 1.5);


INSERT INTO pack_veggies (id, num_of_pack, space_occupied) 
VALUES 
(6, 1, 0.5),  
(7, 1, 0.2),  
(8, 1, 0.5),  
(9, 1, 0.5);


INSERT INTO unit_price_veggies (id, space_occupied) 
VALUES 
(10, 3),  
(11, 1),  
(12, 0.5),  
(13, 0.8),  
(14, 1.5),  
(15, 2),
(16, 3);

INSERT INTO bunch_veggies (id, num_of_bunch, space_occupied)
VALUES 
(17, 2, 1),  
(18, 1, 0.5),  
(19, 1, 0.2),  
(20, 1, 0.2);

INSERT INTO premade_boxes (id, size, space, price) 
VALUES 
(21, 'Small', 5, 0.50),  
(22, 'Medium', 10, 1.00),  
(23, 'Large', 15, 1.50);

INSERT INTO box_contents (box_id, veggie_id, quantity) 
VALUES 
(21, 1, 3),  
(21, 2, 2),  
(22, 3, 5),  
(22, 4, 3),  
(23, 5, 10),  
(23, 6, 4);



INSERT INTO orders (customer_id, date, status, total) VALUES
(3, '2024-01-15 10:00:00', 'Completed', 45.50), 
(4, '2024-01-20 11:30:00', 'Completed', 20.75), 
(3, '2024-02-05 14:00:00', 'Completed', 30.00), 
(3, '2024-03-10 09:15:00', 'Completed', 25.00), 
(4, '2024-04-15 12:00:00', 'Completed', 15.50), 
(3, '2024-05-05 15:30:00', 'Completed', 55.00), 
(4, '2024-06-01 16:00:00', 'Completed', 10.25), 
(3, '2024-06-15 14:00:00', 'Completed', 40.00), 
(4, '2024-07-20 17:30:00', 'Completed', 22.50), 
(3, '2024-08-10 13:00:00', 'Completed', 75.00),  
(4, '2024-09-01 11:00:00', 'Completed', 18.00),  
(3, '2024-09-15 09:45:00', 'Completed', 60.00),  
(4, '2024-10-25 16:30:00', 'Completed', 30.00),  
(3, '2024-10-27 14:00:00', 'Completed', 55.00),  
(4, '2024-10-30 12:00:00', 'Completed', 20.00);  



INSERT INTO payments (amount, date, customer_id, type) VALUES
(45.50, '2024-01-15 10:05:00', 3, 'credit_card'),  
(20.75, '2024-01-20 11:35:00', 4, 'debit_card'),   
(30.00, '2024-02-05 14:05:00', 3, 'credit_card'),  
(25.00, '2024-03-10 09:20:00', 3, 'debit_card'),   
(15.50, '2024-04-15 12:05:00', 4, 'credit_card'),  
(55.00, '2024-05-05 15:35:00', 3, 'debit_card'),   
(10.25, '2024-06-01 16:05:00', 4, 'credit_card'),  
(40.00, '2024-06-15 14:05:00', 3, 'debit_card'),   
(22.50, '2024-07-20 17:35:00', 4, 'credit_card'),  
(75.00, '2024-08-10 13:05:00', 3, 'debit_card'),   
(18.00, '2024-09-01 11:05:00', 4, 'credit_card'),  
(60.00, '2024-09-15 09:50:00', 3, 'debit_card'),   
(30.00, '2024-10-25 16:35:00', 4, 'credit_card'),  
(55.00, '2024-10-27 14:05:00', 3, 'debit_card'),   
(20.00, '2024-10-30 12:05:00', 4, 'credit_card');  



INSERT INTO order_lines (order_id, item_id, quantity) VALUES
(1, 1, 3),  
(1, 2, 2),  
(2, 3, 2),  
(2, 4, 1),  
(3, 4, 1),  
(3, 5, 3),  
(4, 1, 1),  
(4, 6, 2),  
(5, 6, 3),  
(6, 2, 1),  
(6, 3, 2),  
(7, 7, 3),  
(7, 8, 1),  
(8, 1, 1),  
(8, 10, 2), 
(9, 9, 2),  
(9, 11, 1), 
(10, 10, 1), 
(10, 12, 3), 
(11, 12, 2), 
(11, 13, 1), 
(12, 13, 3), 
(12, 14, 1), 
(13, 14, 2), 
(13, 15, 1), 
(14, 15, 1), 
(14, 16, 5), 
(15, 1, 2),  
(15, 16, 1);  
