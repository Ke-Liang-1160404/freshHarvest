"""! @brief People classes for Fresh Harvest Veggies."""

##
# @mainpage Fresh Harvest Veggies
#
# @section description_main Description
# Fresh Harvest Veggies is a small business that sells fresh produce to customers.
#
# @section notes_main Notes
# - The system includes classes for customers, products, orders, and payments.
# - Customers can be private or corporate customers.
# - Products can be individual items or box products.
# - Orders include a list of products or boxes, a total price, and a delivery status.
# - Payments include an order, amount, and payment method.
# add more notes here

## 
#
# @file People.py
#
# @brief abstract class for all people, and classes for customers and staff.
#
# @section description_people Description
# This file contains the People classes for Fresh Harvest Veggies, including Customer, PrivateCustomer, CorporateCustomer and Staff classes.
#
# @section notes_modal Notes 
# - The Customer class represents a general customer with a customer number, name, and balance.
# - The PrivateCustomer class inherits from Customer and adds a maximum balance limit.
# - The CorporateCustomer class inherits from Customer and adds a credit limit and discount rate.
# - The Staff class represents an employee with a staff ID.
# add more notes here
#
# @section author Author
# Created by Kurt Liang student ID: 1160404 on 24-09-2024.

#imports
from abc import ABC, abstractmethod
from typing import Literal,List,Dict
from freshHarvest.OrderPaymentModels import Order

class People(ABC):
    """! Abstract class for all people. Parent class for roles such as Customer and Staff."""
    def __init__(self, name: str):
        """! Constructor for the People class.
        @param name (str): The name of the person.
        """
        self.__name = name
        
    @property
    def name(self):
        """! Getter for the name attribute.
        @param None
        @return str: The name of the person.
        """
        return self.__name
    @name.setter
    def name(self, value):
        """! Setter for the name attribute.
        @param value (str): The name of the person.
        @return None
        """
        self.__name = value
        
    @abstractmethod
    def role_description(self):
        """! Provide a description of the person's role.
        @param None
        @return str: The description of the role.
        """
        pass


class Customer(People):
    """! inherited from People class. Represents a general customer with a customer number, name, and balance. parent class for PrivateCustomer and CorporateCustomer."""
    def __init__(self, customer_number: int, name: str, balance: float):
        """! Constructor for the Customer class.
        @param customer_number (int): The unique customer number. 
        @param name (str): The name of the customer.
        @param balance (float): The balance of the customer.  
        """
        super().__init__(name)
        self.__customer_number = customer_number
        self.__balance = balance
        self.__orders = [Order]
        
    @property
    def balance(self):
        """! Getter for the balance attribute.
        @param None
        @return float: The balance of the customer."""
        return self.__balance
    @balance.setter
    def balance(self, value):
        """! Setter for the balance attribute.
        @param value: The balance of the customer.
        @return None
        """
        self.__balance = value
        
    @property
    def orders(self):
        """! Getter for the orders attribute.
        @param None
        @return list: A list of all orders for the customer.
        """
        return self.__orders
    @orders.setter
    def orders(self, value):
        """! Setter for the orders attribute.
        @param value: The orders to set.
        @return None
        """
        self.__orders = value
    
    @property
    def name(self):
        """! Getter for the name attribute.
        @param None
        @return str: The name of the customer.
        """
        return self.__name 
    @name.setter
    def name(self, value):
        """! Setter for the name attribute.
        @param value: The name of the customer.
        @return None
        """
        self.__name = value
        
    @property
    def customer_number(self):
        """! Getter for the customer_number attribute.
        @param None
        @return int: The unique customer number.
        """
        return self.__customer_number
    @customer_number.setter
    def customer_number(self, value):
        """! Setter for the customer_number attribute.
        @param value: The unique customer number.
        @return None
        """
        self.__customer_number = value
    
    
    def __str__(self):
        """! String representation of the customer.
        @param None
        @return str: The string representation of the customer.
        """
        return f"Customer {self.customer_number}: {self.name}"
      
    @abstractmethod
    def all_orders(self):
        """! Display all orders for the customer.
        @param None
        @return list: A list of all orders for the customer.
        """
        pass
      
    @abstractmethod
    def create_order(self, order):
        """! Add an order to the customer's list of orders.
        @param order: The order to add.
        @return None
        """
        pass
      
    @abstractmethod
    def all_payments(self):
        """! Display all payments for the customer.
        @param None
        @return list: A list of all payments for the customer.
        """
        pass  
      
    @abstractmethod
    def show_balance(self):
        """! Display the customer's balance.
        @param None
        @return float: The customer's balance.
        """
        pass
      
    def role_description(self):
        """! Provide a description of the customer's role.
        @param None
        @return str: A description of the customer's role.
        """
        pass
      

class Staff(People):
    """! Staff class representing employees in the system. Inherits from the People class and only includes the staff ID. """
    def __init__(self, staff_id: int, name: str):
        """! Constructor for the Staff class.
        @param staff_id (int): The unique staff ID.
        @param name (str): The name of the staff member.
        """
        super().__init__(name)
        self.__staff_id = staff_id

    @property
    def staff_id(self):
        """! Getter for the staff_id attribute.
        @param None
        @return int: The unique staff ID.
        """
        return self.__staff_id

    @staff_id.setter
    def staff_id(self, value):
        """! Setter for the staff_id attribute.
        @param value: The unique staff ID.
        @return None
        """
        self.__staff_id = value

    def __str__(self):
        """! String representation of the staff member.
        @param None
        @return str: The string representation of the staff member.
        """
        return f"Staff {self.staff_id}: {self.name}"
      
    def role_description(self):
        """! Provide a description of the staff member's role.
        @param None
        @return str: A description of the staff member's role.
        """
        pass  
    
    def view_orders(self):
        """! View all orders in the system.
        @param None
        @return list: A list of all orders in the system.
        """
        pass
      
    def view_customers(self):
        """! View all customers in the system.
        @param None
        @return list: A list of all customers in the system.
        """
        pass
      
    def view_products(self):
        """! View all products in the system.
        @param None
        @return list: A list of all products in the system.
        """
        pass
      
    def view_payments(self):
        """! View all payments in the system.
        @param None
        @return list: A list of all payments in the system.
        """
        pass
    
 
      
      
    


class PrivateCustomer(Customer):
    """! private customer class. Inherits from Customer."""
    def __init__(self, customer_number: int, name: str, balance: float, owing: float = 100.00):
        """! Constructor for the PrivateCustomer class. 
        @param customer_number (int): The unique customer number.
        @param name (str): The name of the customer.
        @param balance (float): The balance of the private customer.
        @param owing (float): Private customers cannot place orders if the amount owing is greater than $100.00
        """
        super().__init__(customer_number, name, balance)
        self.__owing = owing
        
    @property
    def owing(self):
        """! Getter for the owing attribute.
        @param None
        @return float: The amount owing for the private customer.
        """
        return self.__owing
    @owing.setter
    def owing(self, value):
        """! Setter for the owing attribute.
        @param value: The amount owing for the private customer.
        @return None
        """
        self.__owing = value
    
    def __str__(self):
        """! String representation of the private customer.
        @param None
        @return str: The string representation of the private customer.
        """
        
        return f"Private Customer {self.customer_number}: {self.name}"
    
      
        
    def all_orders(self):
        """! Display all orders for the private customer.
        @param None
        @return list: A list of all orders for the private customer.
        """
        pass
    
    def all_payments(self):
        """! Display all payments for the private customer.
        @param None
        @return list: A list of all payments for the private customer.
        """
        pass
      
    def show_balance(self):
        """! Display the private customer's balance.
        @param None
        @return float: The private customer's balance.
        """
        pass
      
    def create_order(self, order) -> bool:
        """! Add an order to the private customer's list of orders.
        @param order: The order to add.
        @return Bool: True if the order is added, False otherwise.
        """
        pass
  
    def role_description(self):
        """! Provide a description of the private customer's role.
        @param None
        @return str: A description of the private customer's role.
        """
        pass

class CorporateCustomer(Customer):
    """! corporate customer class. Inherits from Customer and adds specific rules for corporate customers."""
    def __init__(self, customer_number: int, name: str, balance: float, credit_limit: float, discount_rate: float = 0.1):
        """! Constructor for the CorporateCustomer class.
        @param customer_number (int): The unique customer number.
        @param name (str): The name of the corporate customer.
        @param balance (float): The balance of the corporate customer.  
        @param credit_limit (float): The credit limit for the corporate customer.
        @param discount_rate (float): The discount rate for the corporate customer."""
        super().__init__(customer_number, name, balance)
        self.__credit_limit = credit_limit
        self.__discount_rate = discount_rate
        
    @property
    def credit_limit(self):
        """! Getter for the credit_limit attribute.
        @param None
        @return float: The credit limit for the corporate customer.
        """
        return self.__credit_limit
    @credit_limit.setter
    def credit_limit(self, value):
        """! Setter for the credit_limit attribute
        @param value: The credit limit for the corporate customer.
        @return None"""
        self.__credit_limit = value
    
    @property
    def discount_rate(self):
        """! Getter for the discount_rate attribute.
        @param None
        @return float: The discount rate for the corporate customer.
        """
        return self.__discount_rate
    @discount_rate.setter
    def discount_rate(self, value):
        """! Setter for the discount_rate attribute.
        @param value: The discount rate for the corporate customer.
        @return None"""
        self.__discount_rate = value
    
    def __str__(self):
        """! String representation of the corporate customer.
        @param None
        @return str: The string representation of the corporate customer.
        """
        return f"Corporate Customer {self.customer_number}: {self.name}"  
    
    def apply_discount(self, amount: float) -> float:
        """! Apply a discount to the order total for a corporate customer.
        @param amount (float): The total amount of the order.
        @return float: The discounted amount.
        """
        pass
      
    def all_orders(self):
        """! Display all orders for the corporate customer.
        @param None
        @return list: A list of all orders for the corporate customer.
        """
        pass
    
    def all_payments(self):
        """! Display all payments for the corporate customer.
        @param None
        @return list: A list of all payments for the corporate customer.
        """
        pass
      
    def show_balance(self): 
        """! Display the corporate customer's balance.
        @param None
        @return float: The corporate customer's balance.
        """
        pass
      
    def create_order(self, order) -> bool:
        """! Add an order to the corporate customer's list of orders.
        @param order: The order to add.
        @return Bool: True if the order is added, False otherwise.
        """
        pass
    
    def role_description(self):
        """! Provide a description of the corporate customer's role.
        @param None
        @return str: A description of the corporate customer's role.
        """
        pass  



      
    

