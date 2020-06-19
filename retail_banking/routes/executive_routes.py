from retail_banking import app
from flask import request, render_template, redirect, url_for, flash, jsonify
import retail_banking.models as models
from flask_login import login_required, current_user
from retail_banking.forms import CreateCustomerForm, DepositForm, WithdrawForm, TransferForm, BaseTransactionForm
from retail_banking import db
from retail_banking.errors import NoSuchAccountError


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
            activity = models.CustomerActivity(
                customer_id=customer.id,
                message="Customer Created"
            )
            db.session.add(activity)
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
            activity = models.CustomerActivity(
                customer_id=customer.id,
                message="Customer Updated"
            )
            db.session.add(activity)
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
        activity = models.CustomerActivity(
            customer_id=customer.id,
            message="Customer Deleted"
        )
        db.session.add(activity)
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


def transact(transaction):
    try:
        account = None
        if transaction.operation == models.OPERATIONS['D']:
            account = models.Account.query.filter_by(
                id=transaction.account_id, account_type=transaction.des_account_type).first()
        elif transaction.operation == models.OPERATIONS['W']:
            account = models.Account.query.filter_by(
                id=transaction.account_id, account_type=transaction.src_account_type).first()
        if account and account.status == models.ACC_STATUS['A']:
            db.session.add(transaction)
            db.session.commit()
            if transaction.operation == models.OPERATIONS['D']:
                account.balance += transaction.amount
            elif transaction.operation == models.OPERATIONS['W']:
                account.balance -= transaction.amount
            db.session.commit()
            flash("{} of Amount {} completed successfully".format(
                transaction.operation, str(transaction.amount)), 'success')
        else:
            raise NoSuchAccountError()
    except NoSuchAccountError as e:
        flash(str(e), 'error')
    except Exception as e:
        flash(str(e), 'error')


@app.route("/transaction/<string:operation>/", methods=["POST", "GET"])
def transaction(operation):
    form = None
    transaction = models.Transaction()
    if operation == "deposit":
        form = DepositForm()
        if form.validate_on_submit():
            transaction.account_id = form.account_id.data
            transaction.des_account_type = form.des_account_type.data
            transaction.amount = form.amount.data
            transaction.operation = models.OPERATIONS['D']
            transact(transaction)
    elif operation == "withdraw":
        form = WithdrawForm()
        if form.validate_on_submit():
            transaction.account_id = form.account_id.data
            transaction.src_account_type = form.src_account_type.data
            transaction.amount = form.amount.data
            transaction.operation = models.OPERATIONS['W']
            transact(transaction)
    # elif operation == "transfer":
    #     form = TransferForm()
    #     if form.validate_on_submit():
    #         transaction.account_id = form.account_id.data
    #         transaction.src_account_type = form.src_account_type.data
    #         transaction.des_account_type = form.des_account_type.data
    #         transaction.amount = form.amount.data
    #         transaction.operation = models.OPERATIONS['D']
    #         transact(transaction)
    return render_template('cashier/transaction.html', form=form, title=operation, operation=operation)
