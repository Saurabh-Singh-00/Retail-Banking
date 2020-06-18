from retail_banking import app
from flask import render_template, redirect, render_template, url_for, flash, request
from retail_banking.routes import executive_routes
from retail_banking.routes import cashier_routes
from flask_login import current_user, login_user, logout_user
from retail_banking.forms import LoginForm
from retail_banking.models import Employee


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Employee.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/index")
def index():
    return render_template("base.html")

@app.route("/newcustomer/")
def Customer():
    return render_template("NewCustomer.html")

@app.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.is_executive:
        return render_template('executive/home.html')
    return render_template('cashier/home.html')
