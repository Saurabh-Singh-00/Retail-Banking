from retail_banking import app
from flask import request
import retail_banking.models as models


@app.route("/customer_status", methods=["GET"])
def customer_status():
    return ""
