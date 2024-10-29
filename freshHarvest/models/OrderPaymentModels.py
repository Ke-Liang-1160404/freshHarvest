from freshHarvest import db
from datetime import datetime
from freshHarvest.models.ProductModels import Item


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

class CreditCardPayment(Payment):
    __tablename__ = 'credit_card_payments'
    id = db.Column(db.Integer, db.ForeignKey('payments.id'), primary_key=True)
    card_number = db.Column(db.String(16), nullable=False)
    card_type = db.Column(db.String(20))
    expiry_date = db.Column(db.String(5))  # MM/YY

class DebitCardPayment(Payment):
    __tablename__ = 'debit_card_payments'
    id = db.Column(db.Integer, db.ForeignKey('payments.id'), primary_key=True)
    bank_name = db.Column(db.String(100))
    card_number = db.Column(db.String(16))

# --- Order and OrderLine ---
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')
    total= db.Column(db.Float, nullable=False)    
    items = db.relationship('OrderLine', backref='order')
    
    def __init__(self, customer_id): 
        self.customer_id = customer_id
        self.total = self.order_total()
    
    def order_total(self):
        total = 0
        for order_line in self.items:
            total += order_line.order_line_total()
            total_price= round(total, 2)
        return total_price

class OrderLine(db.Model):
    __tablename__ = 'order_lines'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    quantity = db.Column(db.Integer, nullable=False)
    
    item = db.relationship('Item', backref='order_lines')
    
    def __init__ (self, order_id, item_id, quantity):
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity
    
    def order_line_total(self):
        veggie= Item.query.get(self.item_id) 
        if veggie.price:
            total_price=veggie.price * self.quantity
            print(total_price)
            total=round(total_price, 2)
            return total
        else:
            raise ValueError("Item does not have a price attribute.")
          
    def __repr__(self):
        return f"OrderLine({self.order_id}, {self.item_id}, {self.quantity})"