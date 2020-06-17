from retail_banking import app
from flask import render_template
from retail_banking.routes import executive_routes
from retail_banking.routes import cashier_routes


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return "Hello World!"
