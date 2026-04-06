from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..extensions import db
from ..models import Child


children_bp = Blueprint("children", __name__, url_prefix="/children")


@children_bp.get("/")
def list_children():
    children = Child.query.order_by(Child.name).all()
    return render_template("children/list.html", children=children)


@children_bp.route("/new", methods=["GET", "POST"])
def create_child():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        color = request.form.get("color", "blue").strip() or "blue"
        is_active = bool(request.form.get("is_active"))

        if not name:
            flash("El nombre es obligatorio.", "error")
            return render_template("children/form.html", child=None)

        if Child.query.filter_by(name=name).first():
            flash("Ya existe una hija con ese nombre.", "error")
            return render_template("children/form.html", child=None)

        db.session.add(Child(name=name, color=color, is_active=is_active))
        db.session.commit()
        flash("Hija creada correctamente.", "success")
        return redirect(url_for("children.list_children"))

    return render_template("children/form.html", child=None)


@children_bp.route("/<int:child_id>/edit", methods=["GET", "POST"])
def edit_child(child_id: int):
    child = Child.query.get_or_404(child_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        color = request.form.get("color", "blue").strip() or "blue"
        is_active = bool(request.form.get("is_active"))

        if not name:
            flash("El nombre es obligatorio.", "error")
            return render_template("children/form.html", child=child)

        existing = Child.query.filter(Child.name == name, Child.id != child.id).first()
        if existing:
            flash("Ya existe otra hija con ese nombre.", "error")
            return render_template("children/form.html", child=child)

        child.name = name
        child.color = color
        child.is_active = is_active
        db.session.commit()
        flash("Hija actualizada correctamente.", "success")
        return redirect(url_for("children.list_children"))

    return render_template("children/form.html", child=child)


@children_bp.post("/<int:child_id>/delete")
def delete_child(child_id: int):
    child = Child.query.get_or_404(child_id)
    db.session.delete(child)
    db.session.commit()
    flash("Hija eliminada correctamente.", "success")
    return redirect(url_for("children.list_children"))
