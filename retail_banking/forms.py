from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField

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
