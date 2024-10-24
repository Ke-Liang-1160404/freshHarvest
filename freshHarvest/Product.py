"""! @brief Product classes for Fresh Harvest Veggies."""
## 
# @file Product.py
#
# @brief Product classes for Fresh Harvest Veggies, including Product and BoxProduct.
#
# @section description_Product Description
# This file contains the Product, BoxProduct classes for Fresh Harvest Veggies.
# BoxProduct is a special type of product with specific size that can contain multiple products with quantities. and the Product class represents a product with a product ID, name, price per unit, and unit.
#
# @section notes_modal Notes 
# - The Product class represents a product with a product ID, name, price per unit, and unit.
# - The BoxProduct class represents a box product with a size and products with quantities.
# add more notes here
#
# @section author Author
# Created by Kurt Liang student ID: 1160404 on 24-09-2024.

#import
from typing import Literal


class Product():
    """! class for product."""
    
    def __init__(self, product_id: int, name: str, price_per_unit: float, unit: Literal['pack', 'punnet', 'weight', 'bunches']):
        """! Constructor for the Product class.
        @param product_id (int): The unique product ID.
        @param name (str): The name of the product.
        @param price_per_unit (float): Price of one unit of the product.
        @param unit (str): The unit of the product (e.g., 'pack', 'punnet', 'weight', 'bunches').
        """
        self.__product_id = product_id
        self.__name = name
        self.__price_per_unit = price_per_unit
        self.__unit = unit
        
    @property
    def product_id(self): 
        """! Getter for the product_id attribute.
        @param None
        @return int: The product_id
        """
        return self.__product_id
    @product_id.setter
    def product_id(self, value):
        """! Setter for the product_id attribute.
        @param value: The product_id.
        @return None
        """
        self.__product_id = value
    
    @property
    def name(self):
        """! Getter for the name attribute.
        @param None
        @return str: The name of the product.
        """
        return self.__name
      
    @name.setter
    def name(self, value):
        """! Setter for the name attribute.
        @param value: The name of the product.
        @return None
        """
        
        self.__name = value
    
    @property
    def price_per_unit(self):
        """! Getter for the price_per_unit attribute.
        @param None
        @return float: The price of one unit of the product.
        """
        return self.__price_per_unit
    @price_per_unit.setter
    def price_per_unit(self, value):
        """! Setter for the price_per_unit attribute.
        @param value: The price of one unit of the product.
        @return None"""
        self.__price_per_unit = value
    
    @property
    def unit(self):
        """! Getter for the unit attribute.
        @param None
        @return str: The unit of the product.
        """
        return self.__unit
    @unit.setter  
    def unit(self, value):
        """! Setter for the unit attribute.
        @param value: The unit of the product.
        @return None
        """
        self.__unit = value
        
    def __str__(self):
        """! String representation of the product.
        @param None
        @return str: The string representation of the product.
        """
        
        return f"Product {self.product_id}: {self.name} (${self.price_per_unit}/{self.unit})"
      
   
      
      

    
        

class BoxProduct():
    """! class for box product.
    a box can contain multiple products with quantities.
    for example, a box can contain 2 kg of apples, 3 packs of potatoes, 2 bunches of coriander.
    """
    def __init__(self, size: str ):
        """! Constructor for the BoxProduct class.
        @param size (str): The size of the box (small, medium, large).
        """
        self.__size = size
        self.__products = {}  # Dictionary of products and their quantities

        
    @property
    def size(self):
        """! Getter for the size attribute.
        @param None
        @return str: The size of the box.
        """
        return self.__size
    @size.setter
    def size(self, value):
        """! Setter for the size attribute.
        @param value: The size of the box.
        @return None
        """
        self.__size = value
        
    @property
    def products(self):
        """! Getter for the products attribute.
        @param None
        @return dict: A dictionary of products and their quantities.
        """
        return self.__products
        

        
    def __str__(self):
        """! String representation of the box product.
        @param None
        @return str: The string representation of the box product."""
        return f"Box ({self.size}) - Total: ${self.price:.2f}"  
          
    def calculate_total(self) -> float:
        """! Calculate the total price of the premade box based on its contents.
        @param None
        @return float: The total price of all the products inside the box.
        """
        pass
        
    def all_products(self):
        """! Display all products in the box.
        @param None
        @return dict: A dictionary of products and their quantities.
        """
        pass
      
    def add_product(self, product: Product, quantity: int):
        """! Add a product to the box.
        @param product: The product to add.
        @param quantity: The quantity of the product to add.
        @return None
        """
        pass
      
    def remove_product(self, product: Product):
        """! Remove a product from the box.
        @param product: The product to remove.
        @return None
        """
        pass