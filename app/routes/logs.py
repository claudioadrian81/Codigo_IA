from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..extensions import db
from ..models import Activity, ActivityLog, Child


logs_bp = Blueprint("logs", __name__, url_prefix="/logs")


@logs_bp.route("/new", methods=["GET", "POST"])
def create_log():
    active_children = Child.query.filter_by(is_active=True).order_by(Child.name).all()
    active_activities = Activity.query.filter_by(is_active=True).order_by(Activity.name).all()

    if request.method == "POST":
        child_id = request.form.get("child_id", type=int)
        activity_id = request.form.get("activity_id", type=int)
        performed_at_str = request.form.get("performed_at", "").strip()
        notes = request.form.get("notes", "").strip()

        child = Child.query.get(child_id) if child_id else None
        activity = Activity.query.get(activity_id) if activity_id else None

        if not child or not activity:
            flash("Debes seleccionar una hija y una actividad válidas.", "error")
            return render_template(
                "logs/form.html",
                children=active_children,
                activities=active_activities,
            )

        try:
            performed_at = datetime.fromisoformat(performed_at_str)
        except ValueError:
            flash("Fecha/hora inválida.", "error")
            return render_template(
                "logs/form.html",
                children=active_children,
                activities=active_activities,
            )

        log = ActivityLog(
            child_id=child.id,
            activity_id=activity.id,
            reward_minutes_snapshot=activity.reward_minutes,
            performed_at=performed_at,
            notes=notes,
        )
        db.session.add(log)
        db.session.commit()
        flash("Actividad registrada correctamente.", "success")
        return redirect(url_for("logs.history"))

    return render_template("logs/form.html", children=active_children, activities=active_activities)


@logs_bp.get("/history")
def history():
    child_id = request.args.get("child_id", type=int)
    activity_id = request.args.get("activity_id", type=int)
    date_from_str = request.args.get("date_from", "").strip()
    date_to_str = request.args.get("date_to", "").strip()

    query = ActivityLog.query.join(Child).join(Activity)

    if child_id:
        query = query.filter(ActivityLog.child_id == child_id)
    if activity_id:
        query = query.filter(ActivityLog.activity_id == activity_id)

    if date_from_str:
        try:
            date_from = datetime.fromisoformat(f"{date_from_str}T00:00")
            query = query.filter(ActivityLog.performed_at >= date_from)
        except ValueError:
            flash("Fecha desde inválida.", "error")

    if date_to_str:
        try:
            date_to = datetime.fromisoformat(f"{date_to_str}T23:59")
            query = query.filter(ActivityLog.performed_at <= date_to)
        except ValueError:
            flash("Fecha hasta inválida.", "error")

    logs = query.order_by(ActivityLog.performed_at.desc()).all()
    children = Child.query.order_by(Child.name).all()
    activities = Activity.query.order_by(Activity.name).all()

    return render_template(
        "logs/history.html",
        logs=logs,
        children=children,
        activities=activities,
        filters={
            "child_id": child_id,
            "activity_id": activity_id,
            "date_from": date_from_str,
            "date_to": date_to_str,
        },
    )


@logs_bp.post("/<int:log_id>/delete")
def delete_log(log_id: int):
    log = ActivityLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash("Registro eliminado correctamente.", "success")
    return redirect(url_for("logs.history"))
