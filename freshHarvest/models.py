from freshHarvest import db
import datetime
from freshHarvest import ma

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date= db.Column(db.DateTime,default=datetime.datetime.now, nullable=False) 
    
    def __init__(self, name,email) -> None:
        super().__init__()  
        self.name = name
        self.email = email
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','date')
 
user_schema = UserSchema()
users_schema = UserSchema(many=True)