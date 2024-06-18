from flask import Flask
from models import mysql, bcrypt, init_app
from routes import main_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pramod2805'
app.config['MYSQL_DB'] = 'lab_tests'

init_app(app)
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
