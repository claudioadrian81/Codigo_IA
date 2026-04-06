from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..extensions import db
from ..models import Activity


activities_bp = Blueprint("activities", __name__, url_prefix="/activities")


@activities_bp.get("/")
def list_activities():
    activities = Activity.query.order_by(Activity.name).all()
    return render_template("activities/list.html", activities=activities)


@activities_bp.route("/new", methods=["GET", "POST"])
def create_activity():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        reward_minutes = request.form.get("reward_minutes", "0").strip()
        is_active = bool(request.form.get("is_active"))

        if not name:
            flash("El nombre es obligatorio.", "error")
            return render_template("activities/form.html", activity=None)

        if Activity.query.filter_by(name=name).first():
            flash("Ya existe una actividad con ese nombre.", "error")
            return render_template("activities/form.html", activity=None)

        try:
            reward_minutes_val = int(reward_minutes)
            if reward_minutes_val <= 0:
                raise ValueError
        except ValueError:
            flash("Los minutos deben ser un entero mayor a 0.", "error")
            return render_template("activities/form.html", activity=None)

        db.session.add(
            Activity(
                name=name,
                description=description,
                reward_minutes=reward_minutes_val,
                is_active=is_active,
            )
        )
        db.session.commit()
        flash("Actividad creada correctamente.", "success")
        return redirect(url_for("activities.list_activities"))

    return render_template("activities/form.html", activity=None)


@activities_bp.route("/<int:activity_id>/edit", methods=["GET", "POST"])
def edit_activity(activity_id: int):
    activity = Activity.query.get_or_404(activity_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        reward_minutes = request.form.get("reward_minutes", "0").strip()
        is_active = bool(request.form.get("is_active"))

        if not name:
            flash("El nombre es obligatorio.", "error")
            return render_template("activities/form.html", activity=activity)

        existing = Activity.query.filter(Activity.name == name, Activity.id != activity.id).first()
        if existing:
            flash("Ya existe otra actividad con ese nombre.", "error")
            return render_template("activities/form.html", activity=activity)

        try:
            reward_minutes_val = int(reward_minutes)
            if reward_minutes_val <= 0:
                raise ValueError
        except ValueError:
            flash("Los minutos deben ser un entero mayor a 0.", "error")
            return render_template("activities/form.html", activity=activity)

        activity.name = name
        activity.description = description
        activity.reward_minutes = reward_minutes_val
        activity.is_active = is_active
        db.session.commit()
        flash("Actividad actualizada correctamente.", "success")
        return redirect(url_for("activities.list_activities"))

    return render_template("activities/form.html", activity=activity)


@activities_bp.post("/<int:activity_id>/delete")
def delete_activity(activity_id: int):
    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()
    flash("Actividad eliminada correctamente.", "success")
    return redirect(url_for("activities.list_activities"))
