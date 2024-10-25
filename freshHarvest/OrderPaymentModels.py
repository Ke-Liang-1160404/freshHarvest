"""! @brief Order and Payment classes for Fresh Harvest Veggies."""
## 
# @file OrderPayment.py
#
# @brief OrderPayment classes for Fresh Harvest Veggies.
#
# @section description_OrderPayment Description
# This file contains the Order, OrderItem and Payment  classes for Fresh Harvest Veggies.
# Order is a class that represents an order with an order ID, customer, products, total price, and delivery status.
# OrderItem is a class that represents an order item with an order ID, product or box, and quantity. it can be a product or a box.
# Payment is a class that represents a payment with a payment ID, order, amount, and payment method.
#
# @section notes_modal Notes 
# - The Order class represents an order with an order ID, customer, products, total price, and delivery status.
# - The Payment class represents a payment with a payment ID, order, amount, and payment method.
# - The OrderItem class represents an order item with an order ID, product or box, and quantity.
# add more notes here
#
# @section author Author
# Created by Kurt Liang student ID: 1160404 on 24-09-2024.


#import
from freshHarvest.ProductModels import Product, BoxProduct
from freshHarvest.PeopleModels import Customer
from typing import Literal
from freshHarvest import db

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    order_item_id = db.Column(db.Integer, primary_key=True)
    product_or_box_id = db.Column(db.Integer, nullable=False)
    product_type= db.Column(db.String(100))
    quantity = db.Column(db.Integer, nullable=False)  # distinguish between product and boxProduct
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    order = db.relationship('Orders', back_populates='order_items')


    __mapper_args__ = {
        'polymorphic_identity': 'order_item',
        'polymorphic_on': product_type
    }
    """! class for order item. 
    an order item can be a product or a box.
    """
    
    def __init__(self, product_or_box, quantity: int = 1):
        """! Constructor for the OrderItem class. 
        @param product_or_box: Can be either a Product or a BoxProduct.
        @param quantity (int): Quantity of the product or the box.
        """
        self.__product_or_box = product_or_box
        self.__quantity = quantity

    @property
    def order_id(self):
        """! Getter for the order_id attribute.
        @param None
        @return int: The order_id
        """
        return self.__order_id
    @order_id.setter
    def order_id(self, value):
        """! Setter for the order_id attribute.
        @param value: The order_id.
        @return None"""
        self.__order_id = value
        
    @property
    def product_or_box(self):
        """! Getter for the product_or_box attribute.
        @param None
        @return Product | BoxProduct: The product or box.
        """
        
        return self.__product_or_box
      
    @product_or_box.setter
    def product_or_box(self, value):
        """! Setter for the product_or_box attribute.
        @param value: The product or box.
        @return None
        """
        self.__product_or_box = value
      
    @property
    def quantity(self):
        """! Getter for the quantity attribute."""
        return self.__quantity
    @quantity.setter
    def quantity(self, value):
        """! Setter for the quantity attribute.
        @param value: The quantity of the product or box.
        @return None
        """
        self.__quantity = value

    def __str__(self):
        """! String representation of the order item."""
        return f"OrderItem {self.order_id}: {self.product_or_box} x {self.quantity} - Total: ${self.total_price:.2f}"

    def calculate_total(self) -> float:
        """! Calculate the total price for this order item.
        @param None
        @return float: The total price of the product or box in the order.
        """
        pass
      
class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    delivery_distance = db.Column(db.Float)
    
    customer = db.relationship('Customer', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='orders', cascade='all, delete-orphan')


    """! class for order.
    an order can contain multiple order items.
    """
    DELIVERY_FEE = 10.00
    MAX_DELIVERY_DISTANCE = 20.00
    
    def __init__(self, order_id: int, customer: Customer, delivery_distance: float = 0.0):
        """! Constructor for the Order class.
        @param order_id (int): The unique order ID.
        @param customer (Customer): The customer placing the order.

        @param delivery_distance (float): The distance for delivery.
        """
        self.__order_id = order_id
        self.__customer = customer
        self.__order_items = [OrderItem]  # List of OrderItem objects
        self.__delivery_distance = delivery_distance

    @property
    def order_id(self):
        """! Getter for the order_id attribute.
        @param None
        @return int: The order_id
        """
        return self.__order_id
    @order_id.setter
    def order_id(self, value):
        """! Setter for the order_id attribute.
        @param value: The order_id.
        @return None
        """
        self.__order_id = value
    
    @property
    def customer(self):
        """! Getter for the customer attribute.
        @param None
        @return Customer: The customer placing the order.

        """
        return self.__customer
    @customer.setter
    def customer(self, value):
        """! Setter for the customer attribute.
        @param value: The customer placing the order.
        @return None

        """
        self.__customer = value
        
    @property
    def order_items(self):
        """! Getter for the order_items attribute.
        @param None
        @return list: A list of OrderItem objects.

        """
        return self.__order_items

    @property
    def delivery_distance(self):
        """! Getter for the delivery_distance attribute.
        @param None
        @return float: The distance for delivery.

        """
        return self.__delivery_distance
      
    @delivery_distance.setter
    def delivery_distance(self, value):
        """! Setter for the delivery_distance attribute.
        @param value: The distance for delivery.
        @return None

        """
        self.__delivery_distance = value
    
    
    def __str__(self):
        """! String representation of the order.
        @param None
        @return str: The string representation of the order.
        """
        return f"Order {self.order_id} - Total: ${self.total_price:.2f}"
      
    def calculate_total(self,customer) -> float:
        """! Calculate the total price for all order items, including delivery if applicable.
        @param customer, base on customer type to decide discount or not.
        @return float: The total price for the order.
        """
        pass
      
    def add_order_item(self, order_item: OrderItem):
        """! Add an order item to the order.
        @param order_item: The order item to add.
        @return None
        """
        pass
      
    def remove_order_item(self, order_item: OrderItem):
        """! Remove an order item from the order.
        @param order_item: The order item to remove.
        @return None
        """
        pass

    def process_order(self) -> bool:
        """! Process the order if the customer can place it.
        @param None
        @return bool: True if the order is successful, False otherwise.
        """
        pass



class Payment(db.Model):
    __tablename__ = 'payment' 
    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    amount = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    payment_method = db.Column(db.String(100), nullable=False)  # credit, debit, account
    status = db.Column(db.Boolean)  
    
    order = db.relationship('Order', backref='payment')
    """! class for payment"""
    def __init__(self, payment_id: int, order: Order, amount: float, payment_method: Literal ['credit','debit', 'account'], customer: Customer, status: bool = False):
        """! Constructor for the Payment class.
        @param payment_id (int): The unique payment ID.
        @param order (Order): The order being paid.
        @param amount (float): The amount of the payment.
        @param payment_method (str): The payment method.
        @param customer (Customer): The customer making the payment.
        @param status (bool): The status of the payment.
        """
        self.__payment_id = payment_id
        self.__customer = customer
        self.__order = order
        self.__amount = amount
        self.__payment_method = payment_method
        self.__status = status
        
    @property
    def status(self):
        """! Getter for the status attribute.
        @param None
        @return bool: The status of the payment.
        """
        return self.__status
    @status.setter
    def status(self, value):
        """! Setter for the status attribute.
        @param value: The status of the payment.
        @return None
        """
        self.__status = value
        
    @property
    def customer(self):
        """! Getter for the customer attribute.
        @param None
        @return Customer: The customer making the payment.
        """
        return self.__customer
      
    @customer.setter
    def customer(self, value):
        """! Setter for the customer attribute.
        @param value: The customer making the payment.
        @return None
        """
        self.__customer = value
    
    @property
    def  payment_id(self):
        """! Getter for the payment_id attribute.
        @param None
@


        @return int: The payment_id
        """
        return self.__payment_id
    @payment_id.setter
    def payment_id(self, value):
        """! Setter for the payment_id attribute.
        @param value: The payment_id.
        @return None
        """
        self.__payment_id = value
      
    @property
    def order(self):
        """! Getter for the order attribute.
        @param None
        @return Order: The order being paid.
        """
        return self.__order
    @order.setter
    def order(self, value):
        """! Setter for the order attribute.
        @param value: The order being paid.
        @return None
        """
        self.__order = value
    
    @property
    def amount(self):
        """! Getter for the amount attribute.
        @param None
        @return float: The amount of the payment.
        """
        return self.__amount
      
    @amount.setter
    def amount(self, value):
        """! Setter for the amount attribute.
        @param value: The amount of the payment.
        @return None
        """
        self.__amount = value
    @property
    def payment_method(self):
        """! Getter for the payment_method attribute.
        @param None
        @return str: The payment method.  
        """
        return self.__payment_method
    @payment_method.setter
    def payment_method(self, value):
        """! Setter for the payment_method attribute.
        @param value: The payment method.
        @return None
        """
        self.__payment_method = value

    def process_payment(self) -> bool:
        """! Process the payment.
        @param None
        @return bool: True if the payment is successful, False otherwise.
        
        """
        pass


class CreditCardPayment(Payment, db.Model):
    __tablename__ = 'credit_card_payment'
    card_number = db.Column(db.String(100))
    card_expiry = db.Column(db.String(100))
    card_cvv = db.Column(db.String(100))
    
    """! class for credit card payment"""
    def __init__(self, payment_id: int, order: Order, amount: float, payment_method: str, customer: Customer,  card_number: str, card_expiry: str, card_cvv: str, status: bool = False):
        """! Constructor for the CreditCardPayment class.
        @param card_number (str): The credit card number.
        @param card_expiry (str): The credit card expiry date.
        @param card_cvv (str): The credit card CVV.
        """
        super().__init__(payment_id, order, amount, payment_method, customer, status)
        self.__card_number = card_number
        self.__card_expiry = card_expiry
        self.__card_cvv = card_cvv

    @property
    def card_number(self):
        """! Getter for the card_number attribute.
        @param None
        @return str: The credit card number.
        """
        return self.__card_number
    @card_number.setter
    def card_number(self, value):
        """! Setter for the card_number attribute.
        @param value: The credit card number.
        @return None
        """
        self.__card_number = value
      
    @property
    def card_expiry(self):
        """! Getter for the card_expiry attribute.
        @param None
        @return str: The credit card expiry date.
        """
        return self.__card_expiry
    @card_expiry.setter
    def card_expiry(self, value):
        """! Setter for the card_expiry attribute.
        @param value: The credit card expiry date.
        @return None
        """
        self.__card_expiry = value
      
    @property
    def card_cvv(self):
        """! Getter for the card_cvv attribute.
        @param None
        @return str: The credit card CVV.
        """
        return self.__card_cvv
    @card_cvv.setter
    def card_cvv(self, value):
        """! Setter for the card_cvv attribute.
        @param value: The credit card CVV.
        @return None
        """
        self.__card_cvv = value

    def process_payment(self) -> bool:
        """! Process the credit card payment.
        @param None
        @return bool: True if the payment is successful, False otherwise.
        """
        pass
      
      
class DebitCardPayment(Payment,db.Model):
  __tablename__ = 'debt_card_payment'
  card_number = db.Column(db.String(100))
  bank_name = db.Column(db.String(100))
  """! class for debt card payment"""
  def __init__(self, payment_id: int, order: Order, amount: float, payment_method: str, customer: Customer,card_number: str, bank_name:str, status: bool = False, ):
    """! Constructor for the DebtCardPayment class.
    @param card_number (str): The debt card number.
    @param bank_name (str): The bank name.  
    """
    super().__init__(payment_id, order, amount, payment_method, customer, status)
    self.__card_number = card_number
    self.__bank_name = bank_name
    



  @property
  def card_number(self):
    """! Getter for the card_number attribute.
    @param None
    @return str: The debt card number.
    """
    return self.__card_number
  @card_number.setter
  def card_number(self, value):
    """! Setter for the card_number attribute.
    @param value: The debt card number.
    @return None
    """
    self.__card_number = value
  
  @property 
  def bank_name(self):
    """! Getter for the bank_name attribute.
    @param None
    @return str: The bank name.
    """
    return self.__bank_name
  @bank_name.setter
  def bank_name(self, value):
    """! Setter for the bank_name attribute.
    @param value: The bank name.
    @return None
    """
    self.__bank_name = value  

  def process_payment(self) -> bool:
    """! Process the debt card payment.
    @param None
    @return bool: True if the payment is successful, False otherwise.
    """
    pass  
