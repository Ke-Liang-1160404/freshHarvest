CREATE DATABASE freshHarvest;
USE freshHarvest;

CREATE TABLE people (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(128)NOT NULL
);


CREATE TABLE customer (
    customer_id INTEGER PRIMARY KEY,
    balance FLOAT DEFAULT 0.0,
    people_id INTEGER,
    FOREIGN KEY (people_id) REFERENCES people (id)
);

CREATE TABLE private_customer (
    private_id INTEGER PRIMARY KEY,
    owing FLOAT DEFAULT 100.0,
    FOREIGN KEY (private_id) REFERENCES customer (customer_id)
);

CREATE TABLE corporate_customer (
    corporate_id INTEGER PRIMARY KEY,
    credit_limit FLOAT,
    discount_rate FLOAT DEFAULT 0.1,
    FOREIGN KEY (corporate_id) REFERENCES customer (customer_id)
);

CREATE TABLE staff (
    staff_id INTEGER PRIMARY KEY,
    people_id INTEGER,
    FOREIGN KEY (people_id) REFERENCES people (id)
);  


CREATE TABLE product (
    product_id INT PRIMARY KEY AUTO_INCREMENT,  
    name VARCHAR(100) NOT NULL,                 
    price_per_unit FLOAT NOT NULL,              
    unit VARCHAR(10) NOT NULL                   
);


CREATE TABLE box_product (
    box_product_id INT PRIMARY KEY AUTO_INCREMENT,      
    size VARCHAR(10) NOT NULL                   
);


CREATE TABLE box_product_product (
    box_id INT,                                 
    product_id INT,                             
    quantity INT NOT NULL,                      

    PRIMARY KEY (box_id, product_id),           
    FOREIGN KEY (box_id) REFERENCES box_product(box_product_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(product_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    total_amount FLOAT,
    status VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);

CREATE TABLE order_item (
    order_item_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    box_product_id INTEGER,
    quantity INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product (product_id),
    FOREIGN KEY (box_product_id) REFERENCES box_product (box_product_id),
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
);

CREATE TABLE payment (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    customer_id INTEGER,
    payment_method VARCHAR(100) NOT NULL,
    status BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ON DELETE SET NULL
);


CREATE TABLE credit_card_payment (
    payment_id INT PRIMARY KEY,
    card_number VARCHAR(100) NOT NULL,
    card_expiry VARCHAR(100) NOT NULL,
    card_cvv VARCHAR(100) NOT NULL,
    FOREIGN KEY (payment_id) REFERENCES payment(payment_id) ON DELETE CASCADE
);


CREATE TABLE debit_card_payment (
    payment_id INT PRIMARY KEY,
    card_number VARCHAR(100) NOT NULL,
    bank_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (payment_id) REFERENCES payment(payment_id) ON DELETE CASCADE
);


-- Insert People (Shared by Staff and Customers)
INSERT INTO people (name, password) VALUES 
('John', 'password123'), 
('Jane', 'password123'), 
('Alice', 'password123'), 
('Bob', 'password123'), 
('LincolnUni', 'password123');


INSERT INTO staff (staff_id, people_id) VALUES 
(1, 1), 
(2, 2); 

INSERT INTO customer (customer_id, balance, people_id) VALUES 
(1, 50.00, 3), 
(2, 75.00, 4), 
(3, 1000.00, 5);

INSERT INTO private_customer (private_id, owing) VALUES 
(1, 20.00), 
(2, 0.00);  

INSERT INTO corporate_customer (corporate_id, credit_limit, discount_rate) VALUES 
(3, 5000.00, 0.15);  
