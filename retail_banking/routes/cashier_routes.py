from retail_banking import app
from flask import request, render_template, redirect, url_for, flash, jsonify
import retail_banking.models as models
from flask_login import login_required, current_user
from retail_banking.forms import CreateCustomerForm, CreateAccountForm
from retail_banking import db


@app.route("/account_status", methods=["GET"])
@login_required
def account_status():
    customer_activities = []
    for activity in models.AccountActivity.query.all():
        customer_activities.append(activity.serialize())
    return render_template("cashier/account_status.html", customer_activities=customer_activities)


@app.route("/create_account", methods=["GET", "POST"])
@login_required
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():
        account = models.Account(
            customer_id=form.customer_id.data,
            account_type=form.account_type.data,
            balance=form.balance.data,
            status=form.status.data,
        )
        try:
            db.session.add(account)
            db.session.commit()
            activity = models.AccountActivity(
                account_id=account.id,
                message="ACCOUNT CREATED",
            )
            db.session.add(activity)
            db.session.commit()
            flash('Account created successfully with ID {}'.format(
                str(account.id)), 'success')
        except Exception as e:
            print(e)
            flash('Error - Account with same Customer ID already exists', 'warning')
        return redirect(url_for('create_account'))
    return render_template("cashier/create_account.html", account_route="active", form=form, title="Create Account")


@app.route("/search_account", methods=["GET", "POST"])
@login_required
def search_account():
    return render_template("cashier/search_account.html", operation=request.args.get('operation'))


@app.route("/update_account/<int:id>", methods=["GET", "POST"])
@login_required
def update_account(id):
    account = models.Account.query.get(id)
    form = CreateAccountForm(obj=account)
    if form.validate_on_submit():
        account.customer_id = form.customer_id.data
        account.account_type = form.account_type.data
        account.balance = form.balance.data
        account.status = form.status.data
        try:
            db.session.commit()
            activity = models.AccountActivity(
                account_id=account.id,
                message="ACCOUNT UPDATED",
            )
            db.session.add(activity)
            db.session.commit()
            flash('Account Updated successfully with ID {}'.format(
                str(account.id)), 'success')
        except Exception:
            flash('Error - Customer with same SSN already exists', 'warning')
        return redirect(url_for('update_account', id=id))
    return render_template("cashier/create_account.html", customer_route="active", form=form, title="Update Account")


@app.route("/delete_account/<int:id>/", methods=["GET"])
@login_required
def delete_account(id):
    customer = models.Customer.query.get(id)
    if customer:
        customer.status = models.CUSTOMER_STATUS['C']
        db.session.commit()
        activity = models.AccountActivity(
            account_id=account.id,
            message="ACCOUNT DELETED",
        )
        db.session.add(activity)
        db.session.commit()
        flash('Account deleted successfully', 'success')
    return render_template("cashier/search_account.html", operation="delete")


@app.route("/api/account_details/<int:id>/", methods=["GET"])
@login_required
def account_details(id):
    account_activities = models.Account.query.filter_by(
        id=id, status=models.ACC_STATUS['A']).first()
    if account_activities:
        return jsonify(account_activities.serialize())
    return jsonify({"Error": "No such active user with id {}".format(id)})
