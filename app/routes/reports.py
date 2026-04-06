from flask import Blueprint, render_template

from ..services import reports_data


reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.get("/")
def index():
    data = reports_data()
    return render_template("reports/index.html", **data)
