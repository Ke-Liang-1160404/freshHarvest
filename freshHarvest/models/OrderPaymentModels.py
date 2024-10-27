from freshHarvest import db
from datetime import datetime



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
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')

    items = db.relationship('OrderLine', backref='order')

class OrderLine(db.Model):
    __tablename__ = 'order_lines'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    quantity = db.Column(db.Integer, nullable=False)
    
    item = db.relationship('Item', backref='order_lines')