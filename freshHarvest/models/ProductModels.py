from freshHarvest import db


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
    space_occupied = db.Column(db.Float)

class PackVeggie(Veggie):
    __tablename__ = 'pack_veggies'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    num_of_pack = db.Column(db.Integer)
    price_per_pack = db.Column(db.Float)
    space_occupied = db.Column(db.Float)

class UnitPriceVeggie(Veggie):
    __tablename__ = 'unit_price_veggies'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    price_per_unit = db.Column(db.Float)
    space_occupied = db.Column(db.Float)

class BunchVeggie(Veggie):
    __tablename__ = 'bunch_veggies'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    num_of_bunch = db.Column(db.Integer)
    price_per_bunch = db.Column(db.Float)
    space_occupied = db.Column(db.Float)

# --- Premade Box ---
class PremadeBox(Item):
    __tablename__ = 'premade_boxes'
    id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    size = db.Column(db.String(10))  # Small, Medium, Large
    num_of_boxes = db.Column(db.Integer)
    price = db.Column(db.Float)
    space= db.Column(db.Float)

    contents = db.relationship('BoxContent', backref='box')

class BoxContent(db.Model):
    __tablename__ = 'box_contents'
    id = db.Column(db.Integer, primary_key=True)
    box_id = db.Column(db.Integer, db.ForeignKey('premade_boxes.id'))
    veggie_id = db.Column(db.Integer, db.ForeignKey('veggies.id'))
    quantity = db.Column(db.Integer, nullable=False)
    
    veggie = db.relationship('Veggie', backref='box_contents')
