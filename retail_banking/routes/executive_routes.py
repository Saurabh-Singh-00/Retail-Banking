from retail_banking import app
from flask import request, render_template, redirect, url_for, flash, jsonify
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
        try:
            db.session.add(customer)
            db.session.commit()
            flash('Customer created successfully with ID {}'.format(
                str(customer.id)), 'success')
        except Exception:
            flash('Error - Customer with same SSN already exists', 'warning')
        return redirect(url_for('create_customer'))
    return render_template("executive/create_customer.html", customer_route="active", form=form, title="Create Customer")


@app.route("/search_customer", methods=["GET", "POST"])
@login_required
def search_customer():
    return render_template("executive/search_customer.html", operation=request.args.get('operation'))


@app.route("/update_customer/<int:id>", methods=["GET", "POST"])
@login_required
def update_customer(id):
    customer = models.Customer.query.get(id)
    form = CreateCustomerForm(obj=customer)
    if form.validate_on_submit():
        customer.ssn = form.ssn.data
        customer.name = form.name.data
        customer.dob = form.dob.data
        customer.address = form.address.data
        customer.state = form.state.data
        customer.city = form.city.data
        try:
            db.session.commit()
            flash('Customer Updated successfully with ID {}'.format(
                str(customer.id)), 'success')
        except Exception:
            flash('Error - Customer with same SSN already exists', 'warning')
        return redirect(url_for('update_customer', id=id))
    return render_template("executive/create_customer.html", customer_route="active", form=form, title="Update Customer")


@app.route("/delete_customer/<int:id>/", methods=["GET"])
@login_required
def delete_customer(id):
    customer = models.Customer.query.get(id)
    if customer:
        customer.status = models.CUSTOMER_STATUS['C']
        db.session.commit()
        flash('Customer deleted successfully', 'success')
    return render_template("executive/search_customer.html", operation="delete")


@app.route("/api/customer_details/<int:ssn>/", methods=["GET"])
@login_required
def customer_details(ssn):
    customer = models.Customer.query.filter_by(
        ssn=ssn, status=models.CUSTOMER_STATUS['A']).first()
    if customer:
        return jsonify(customer.serialize())
    return jsonify({"Error": "No such active user with ssn {}".format(ssn)})
