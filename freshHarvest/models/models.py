from datetime import datetime
from freshHarvest import db

# --- Person Base Class ---
class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True, extend_existing=True)
    first_name = db.Column(db.String(50), nullable=False, extend_existing=True)
    last_name = db.Column(db.String(50), nullable=False, extend_existing=True)
    password = db.Column(db.String(100), nullable=False, extend_existing=True)
    username = db.Column(db.String(50), unique=True, nullable=False, extend_existing=True)

# --- Staff Class ---
class Staff(Person):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    dept_name = db.Column(db.String(100))

    customers = db.relationship('Customer', backref='staff')
    orders = db.relationship('Order', backref='staff')

# --- Customer Base Class ---
class Customer(Person):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    address = db.Column(db.String(200))
    balance = db.Column(db.Float, default=0.0)
    max_owing = db.Column(db.Float, default=100.0)  # For private customers

    payments = db.relationship('Payment', backref='customer')
    orders = db.relationship('Order', backref='customer')

class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customers'
    id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    discount_rate = db.Column(db.Float, default=0.1)  # 10% discount
    credit_limit = db.Column(db.Float)
    min_balance = db.Column(db.Float, default=0.0)

# --- Payment Base Class ---
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

# --- Item Base Class ---
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Veggie(Item):
    __tablename__ = 'veggies'
    id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)

class WeightedVeggie(Veggie):
    __tablename__ = 'weighted_veggies'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    weight = db.Column(db.Float)
    price_per_kilo = db.Column(db.Float)

class PackVeggie(Veggie):
    __tablename__ = 'pack_veggies'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    num_of_pack = db.Column(db.Integer)
    price_per_pack = db.Column(db.Float)

class UnitPriceVeggie(Veggie):
    __tablename__ = 'unit_price_veggies'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    price_per_unit = db.Column(db.Float)
    quantity = db.Column(db.Integer)

# --- Premade Box ---
class PremadeBox(Item):
    __tablename__ = 'premade_boxes'
    id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    size = db.Column(db.String(10))  # Small, Medium, Large
    num_of_boxes = db.Column(db.Integer)
    price = db.Column(db.Float)

    contents = db.relationship('BoxContent', backref='box')

class BoxContent(db.Model):
    __tablename__ = 'box_contents'
    id = db.Column(db.Integer, primary_key=True)
    box_id = db.Column(db.Integer, db.ForeignKey('premade_boxes.id'))
    veggie_id = db.Column(db.Integer, db.ForeignKey('veggies.id'))
    quantity = db.Column(db.Integer, nullable=False)
