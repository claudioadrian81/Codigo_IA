from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from ..models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username, is_active=True).first()
        if not user or not user.check_password(password):
            flash("Usuario o contraseña inválidos.", "error")
            return render_template("auth/login.html")

        session["user_id"] = user.id
        session["username"] = user.username
        flash("Sesión iniciada correctamente.", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("auth/login.html")


@auth_bp.get("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("auth.login"))
