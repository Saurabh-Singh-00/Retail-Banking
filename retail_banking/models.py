from retail_banking import db, login_manager
from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey, Float, Date
import datetime
from flask_login import UserMixin

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


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Employee(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.String(80), nullable=False)
    is_executive = db.Column(db.Boolean(), default=False)

    def serialize(self):
        return {'id': self.id,
                'username': self.username,
                'name': self.name,
                'dob': self.dob,
                'is_executive': self.is_executive
                }


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    state = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(256), nullable=False)
    status = db.Column(
        db.String(256), default=CUSTOMER_STATUS['A'])

    def serialize(self):
        return {'id': self.id,
                'ssn': self.ssn,
                'name': self.name,
                'dob': str(self.dob),
                'address': self.address,
                'state': self.state,
                'city': self.city,
                'status': self.status
            }


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    account_type = db.Column(
        db.String(20), default=ACC_TYPE['S'], nullable=False)
    balance = db.Column(db.Float(precision=2), default=0.0)
    status = db.Column(db.String(20), default=ACC_STATUS['A'])

    def serialize(self):
        return {'id': self.id,
                'customer_id': self.customer_id,
                'account_type': self.account_type,
                'balance': self.balance,
                'status': self.status
                }


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src_account_type = db.Column(db.String(20), nullable=True)
    des_account_type = db.Column(db.String(20), nullable=True)
    amount = db.Column(db.Float(precision=2), default=0.0)
    operation = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float(precision=2), default=0.0)

    def serialize(self):
        return {
            'id': self.id,
            'src_account_type': self.src_account_type,
            'des_account_type': self.des_account_type,
            'amount': self.amount,
            'operation': self.operation,
            'balance': self.balance
        }


class CustomerActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'message': self.message,
            'date_time': str(self.date_time),
        }


class AccountActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'message': self.message,
            'date_time': self.date_time,
        }
