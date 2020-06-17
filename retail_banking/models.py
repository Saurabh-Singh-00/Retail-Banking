from retail_banking import db
from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey, Float
import datetime

ACC_TYPE = {
    "S": "SAVING",
    "C": "CURRENT"
}

OPERATIONS = {
    "W": "WITHDRAW",
    "D": "DEPOSIT",
    "T": "TRANSFER"
}

CUSTOMER_STATUS = {
    "A": "ACTIVE",
    "C": "CLOSED"
}

ACC_STATUS = {
    "A": "ACTIVE",
    "P": "PENDING",
    "C": "CLOSED"
}


class Employee(db.Model):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.String(80), nullable=False)
    is_executive = db.Column(db.Boolean(), default=False)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    state = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(256), default=CUSTOMER_STATUS['A'], nullable=False)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    account_type = db.Column(db.String(20), default=ACC_TYPE['S'], nullable=False)
    balance = db.Column(db.Float(precision=2), default=0.0)
    status = db.Column(db.String(20), default=ACC_STATUS['A'])


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src_account_type = db.Column(db.String(20), nullable=True)
    des_account_type = db.Column(db.String(20), nullable=True)
    amount = db.Column(db.Float(precision=2), default=0.0)
    operation = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float(precision=2), default=0.0)


class CustomerActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class AccountActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
