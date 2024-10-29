from freshHarvest import db


# --- Item Base Class ---
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50),nullable=False )
    price = db.Column(db.Float,nullable=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'item'
    }
class Veggie(Item):
    __tablename__ = 'veggies'
    id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'veggie',
        'inherit_condition': (id == Item.id)
    }
    
    def __init__(self, name,price):
        super().__init__(name=name,price=price)
        
        
    def __repr__(self) -> str:
        return f"{self.name}" 

class WeightedVeggie(Veggie):
    __tablename__ = 'weighted_veggies'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    weight = db.Column(db.Float)
    space_occupied = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity': 'WeightedVeggie'
    }
    
    def __init__(self, name, weight, space_occupied, price):
      super().__init__(name=name, price=price  )
      self.__weight = weight
      self.__space_occupied = space_occupied

    
          
      @property
      def weight(self):
          return self.__weight  
      @weight.setter
      def weight(self, weight):
          self.__weight = weight
        
      @property
      def space_occupied(self):
          return self.__space_occupied  
      @space_occupied.setter
      def space_occupied(self, space_occupied):
          self.__space_occupied = space_occupied 
      
      
      

class PackVeggie(Veggie):
    __tablename__ = 'pack_veggies'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    num_of_pack = db.Column(db.Integer)
    space_occupied = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity': 'PackVeggie'
    }
    
    def __init__(self, name, num_of_pack, price, space_occupied):
      super().__init__(name=name, price=price)  
      self.num_of_pack = num_of_pack
      self.space_occupied = space_occupied

    @property
    def num_of_pack(self):
        return self.__num_of_pack

    @num_of_pack.setter
    def num_of_pack(self, num_of_pack):
        self.__num_of_pack = num_of_pack

    @property
    def space_occupied(self):
        return self.__space_occupied

    @space_occupied.setter
    def space_occupied(self, space_occupied):
        self.__space_occupied = space_occupied 
      
class UnitPriceVeggie(Veggie):
    __tablename__ = 'unit_price_veggies'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    space_occupied = db.Column(db.Float)
    
    __mapper_args__ = {
        'polymorphic_identity': 'UnitPriceVeggie'
    }
    def __init__(self, name, price, space_occupied):
      super().__init__(name=name, price=price)
      self.space_occupied = space_occupied    
      
   
    @property
    def num_of_pack(self):
        return self.__num_of_pack
    @num_of_pack.setter 
    def num_of_pack(self, num_of_pack):   
        self.__num_of_pack = num_of_pack

      
    @property
    def space_occupied(self):
        return self.__space_occupied  
    @space_occupied.setter
    def space_occupied(self, space_occupied):
        self.__space_occupied = space_occupied 

class BunchVeggie(Veggie):
    __tablename__ = 'bunch_veggies'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    num_of_bunch = db.Column(db.Integer)
    space_occupied = db.Column(db.Float)
    __mapper_args__ = {
        'polymorphic_identity': 'BunchVeggie'
    }
    
    def __init__(self, name, num_of_bunch, price, space_occupied):
      super().__init__(name=name, price=price)
      self.num_of_bunch = num_of_bunch

      self.space_occupied = space_occupied
      
        
    @property
    def num_of_bunch(self):
        return self.__num_of_bunch  
    @num_of_bunch.setter
    def num_of_bunch(self, num_of_bunch):
        self.__num_of_bunch = num_of_bunch
      
    @property
    def space_occupied(self):
        return self.__space_occupied  
    @space_occupied.setter
    def space_occupied(self, space_occupied):
        self.__space_occupied = space_occupied 

# --- Premade Box ---
class PremadeBox(Item):
    __tablename__ = 'premade_boxes'
    id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    size = db.Column(db.String(10))  # Small, Medium, Large
    num_of_boxes = db.Column(db.Integer)
    space= db.Column(db.Float)

    contents = db.relationship('BoxContent', backref='box')
    __mapper_args__ = {
        'polymorphic_identity': 'PremadeBox'
    }
    
    def __init__(self, name, size, num_of_boxes, price, space):
      super().__init__(name=name, price=price)  
      self.size = size
      self.num_of_boxes = num_of_boxes

      self.space = space


class BoxContent(db.Model):
    __tablename__ = 'box_contents'
    id = db.Column(db.Integer, primary_key=True)
    box_id = db.Column(db.Integer, db.ForeignKey('premade_boxes.id'))
    veggie_id = db.Column(db.Integer, db.ForeignKey('veggies.id'))
    quantity = db.Column(db.Integer, nullable=False)
    
    veggie = db.relationship('Veggie', backref='box_contents')
