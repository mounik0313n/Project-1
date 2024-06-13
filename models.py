from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

mysql = MySQL()
bcrypt = Bcrypt()

def init_app(app):
    mysql.init_app(app)
    bcrypt.init_app(app)
