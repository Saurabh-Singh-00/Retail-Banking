from retail_banking import db
from flask_sqlalchemy.utils import sqlalchemy

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.String(80), nullable=False)
    is_executive = db.Column(db.Boolean(), default=False)


# class Account(db.Model):
#     ...


# class Transaction(db.Model):
#     ...


# class Customer(db.Model):
#     ...


# class Activity(db.Model):
#     ...
