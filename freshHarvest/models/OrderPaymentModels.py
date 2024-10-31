from freshHarvest import db
from datetime import datetime,timezone
from freshHarvest.models.ProductModels import Item


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50), nullable=False) #discriminator='payment_type'
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'payment'
    }

    def __repr__(self):
        return f"Payment({self.amount}, {self.date}, {self.type})"
class CreditCardPayment(Payment):
    __tablename__ = 'credit_card_payments'
    id = db.Column(db.Integer, db.ForeignKey('payments.id'), primary_key=True)
    card_number = db.Column(db.String(16), nullable=False)
    card_type = db.Column(db.String(20))
    expiry_date = db.Column(db.String(5))  # MM/YY

    __mapper_args__ = { 
        'polymorphic_identity': 'credit_card',
        'inherit_condition': (id == Payment.id)
    }
    def __init__(self, amount, customer_id, card_number, card_type, expiry_date):
        super().__init__(amount=amount, customer_id=customer_id)
        self.card_number = card_number
        self.card_type = card_type
        self.expiry_date = expiry_date
        self.type = 'credit_card'

        
    def __repr__(self): 
        return f"CreditCardPayment({self.amount}, {self.customer_id}, {self.card_number}, {self.card_type}, {self.expiry_date}, {self.type})"

class DebitCardPayment(Payment):
    __tablename__ = 'debit_card_payments'
    id = db.Column(db.Integer, db.ForeignKey('payments.id'), primary_key=True)
    bank_name = db.Column(db.String(100))
    card_number = db.Column(db.String(16))
    
    __mapper_args__ = {
        'polymorphic_identity': 'debit_card',
        'inherit_condition': (id == Payment.id)
    }

    def __init__(self, amount, customer_id, bank_name, card_number):
        super().__init__(amount=amount, customer_id=customer_id)
        self.bank_name = bank_name
        self.card_number = card_number
        self.type = 'debit_card'
        
    def __repr__(self): 
        return f"DebitCardPayment({self.amount}, {self.customer_id}, {self.bank_name}, {self.card_number}, {self.type})"  
# --- Order and OrderLine ---
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(50), default='Pending')
    total= db.Column(db.Float, nullable=False)    
    items = db.relationship('OrderLine', backref='order')
    
    def order_total(self):
        total = 0
        for order_line in self.items:
            total += order_line.order_line_total()
        total_price= round(total, 2)
        return total_price
      
    def __init__(self, customer_id): 
        self.customer_id = customer_id
        self.total = self.order_total()
        
    def __repr__(self):
        return f"Order({self.customer_id}, {self.date}, {self.status}, {self.total})"
    

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