from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

app= Flask(__name__)

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:asssks0714@localhost/freshharvest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)

from freshHarvest import home, login

