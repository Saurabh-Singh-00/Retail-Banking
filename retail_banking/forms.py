from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from retail_banking import models


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CreateCustomerForm(FlaskForm):
    ssn = StringField('SSN (Social Security Number)',
                      validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    address = TextField('Address', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CreateAccountForm(FlaskForm):
    customer_id = StringField('Customer ID', validators=[DataRequired()])
    account_type = SelectField('Account type', choices=[
                               (v, v) for k, v in models.ACC_TYPE.items()])
    balance = IntegerField('Balance', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        (v, v) for k, v in models.ACC_STATUS.items()])
    submit = SubmitField('Submit')


class BaseTransactionForm(FlaskForm):
    account_id = IntegerField('Account ID', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DepositForm(BaseTransactionForm):
    des_account_type = SelectField('Destination Account type', choices=[
        (v, v) for k, v in models.ACC_TYPE.items()])
    submit = SubmitField('Submit')


class WithdrawForm(BaseTransactionForm):
    src_account_type = SelectField('Source Account type', choices=[
        (v, v) for k, v in models.ACC_TYPE.items()])


class TransferForm(BaseTransactionForm):
    src_account_type = SelectField('Source Account type', choices=[
        (v, v) for k, v in models.ACC_TYPE.items()])
    des_account_type = SelectField('Destination Account type', choices=[
        (v, v) for k, v in models.ACC_TYPE.items()])
