from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from ..extensions import db
from ..models import User


users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/")
def list_users():
    users = User.query.order_by(User.username).all()
    return render_template("users/list.html", users=users)


@users_bp.route("/new", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        is_active = bool(request.form.get("is_active"))

        if not username or not password:
            flash("Usuario y contraseña son obligatorios.", "error")
            return render_template("users/form.html", user=None)

        if User.query.filter_by(username=username).first():
            flash("Ya existe un usuario con ese nombre.", "error")
            return render_template("users/form.html", user=None)

        user = User(username=username, is_active=is_active)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Usuario creado correctamente.", "success")
        return redirect(url_for("users.list_users"))

    return render_template("users/form.html", user=None)


@users_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id: int):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        is_active = bool(request.form.get("is_active"))

        if not username:
            flash("El usuario es obligatorio.", "error")
            return render_template("users/form.html", user=user)

        existing = User.query.filter(User.username == username, User.id != user.id).first()
        if existing:
            flash("Ya existe otro usuario con ese nombre.", "error")
            return render_template("users/form.html", user=user)

        user.username = username
        user.is_active = is_active
        if password.strip():
            user.set_password(password)

        db.session.commit()
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("users.list_users"))

    return render_template("users/form.html", user=user)


@users_bp.post("/<int:user_id>/delete")
def delete_user(user_id: int):
    user = User.query.get_or_404(user_id)

    if user.id == session.get("user_id"):
        flash("No puedes eliminar el usuario con sesión iniciada.", "error")
        return redirect(url_for("users.list_users"))

    db.session.delete(user)
    db.session.commit()
    flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for("users.list_users"))
