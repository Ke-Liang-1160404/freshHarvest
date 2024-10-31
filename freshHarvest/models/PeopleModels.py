from freshHarvest import db
import datetime



# --- Person Base Class ---
class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)

    customers = db.relationship('Customer', back_populates='person', cascade='all, delete-orphan')
    staff = db.relationship('Staff', back_populates='person', cascade='all, delete-orphan')

# --- Staff Class ---
class Staff(Person):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    date_joined = db.Column(db.DateTime, default=datetime.datetime.now)
    dept_name = db.Column(db.String(100))

    person = db.relationship('Person', back_populates='staff', uselist=False)

# --- Customer Base Class ---
class Customer(Person):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    address = db.Column(db.String(200))
    balance = db.Column(db.Float, default=0.0)
    max_owing = db.Column(db.Float, default=100.0)  # For private customers

    payments = db.relationship('Payment', backref='customer')
    orders = db.relationship('Order', backref='customer')

    person = db.relationship('Person', back_populates='customers', uselist=False)
    corporate_customer = db.relationship("CorporateCustomer", back_populates="customer", uselist=False, foreign_keys="CorporateCustomer.id")

    def __repr__(self):
        return f"Customer({self.id}, {self.first_name}, {self.last_name}, {self.username})"
# --- CorporateCustomer Class ---
class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customers'
    id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    discount_rate = db.Column(db.Float, default=0.1)  # 10% discount
    credit_limit = db.Column(db.Float)
    min_balance = db.Column(db.Float, default=0.0)

    customer = db.relationship('Customer', back_populates='corporate_customer', uselist=False, foreign_keys=[id])
