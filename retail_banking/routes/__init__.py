from retail_banking import app
from flask import render_template
from retail_banking.routes import executive_routes
from retail_banking.routes import cashier_routes


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("layout.html")

@app.route("/newcustomer/")
def Customer():
    return render_template("NewCustomer.html")

