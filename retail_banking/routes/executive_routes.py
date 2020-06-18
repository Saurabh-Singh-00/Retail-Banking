from retail_banking import app
from flask import request, render_template, redirect, url_for, flash
import retail_banking.models as models
from flask_login import login_required, current_user
from retail_banking.forms import CreateCustomerForm
from retail_banking import db


@app.route("/customer_status", methods=["GET"])
@login_required
def customer_status():
    customer_activities = []
    for activity in models.CustomerActivity.query.all():
        customer_activities.append(activity.serialize())
    return render_template("executive/customer_status.html", customer_activities=customer_activities)


@app.route("/create_customer", methods=["GET", "POST"])
@login_required
def create_customer():
    form = CreateCustomerForm()
    if form.validate_on_submit():
        customer = models.Customer(
            ssn=form.ssn.data,
            name=form.name.data,
            dob=form.dob.data,
            address=form.address.data,
            state=form.state.data,
            city=form.city.data,
        )
        db.session.add(customer)
        db.session.commit()
        flash('Customer created successfully with ID {}'.format(
            str(customer.id)), 'success')
        return redirect(url_for('home'))
    return render_template("executive/create_customer.html", form=form, title="Create Customer")
