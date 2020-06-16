from flask import Flask
from retail_banking.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
config = Config()

app.config['SECRET_KEY'] = config.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from retail_banking import routes # Strictly place this import here only
