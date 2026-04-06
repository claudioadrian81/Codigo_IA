from flask import Blueprint, render_template

from ..services import dashboard_summary


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/")
def index():
    data = dashboard_summary()
    return render_template("dashboard.html", **data)
