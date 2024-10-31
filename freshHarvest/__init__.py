from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

import pymysql
pymysql.install_as_MySQLdb()
#load environment variables
load_dotenv('/home/KeLiang1160404/freshHarvest/.env')

# Database configuration from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

print("11111",DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)


app= Flask(__name__)
app.secret_key = 'freshHarvest' 
#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{user}:{password}@{host}/{db_name}'.format(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    db_name=DB_NAME
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)

from freshHarvest import home, login, staff_dashboard, customer_dashboard, products,cart, checkoutPament
from freshHarvest.models import PeopleModels, ProductModels, OrderPaymentModels

