from __future__ import annotations

from datetime import date, datetime, timedelta

from sqlalchemy import func

from .extensions import db
from .models import Activity, ActivityLog, Child


def dashboard_summary() -> dict:
    child_stats = (
        db.session.query(
            Child.id,
            Child.name,
            Child.color,
            func.coalesce(func.sum(ActivityLog.reward_minutes_snapshot), 0).label("minutes"),
            func.count(ActivityLog.id).label("tasks_count"),
        )
        .outerjoin(ActivityLog, ActivityLog.child_id == Child.id)
        .group_by(Child.id)
        .order_by(Child.name)
        .all()
    )

    recent_logs = (
        ActivityLog.query.join(Child).join(Activity)
        .order_by(ActivityLog.performed_at.desc())
        .limit(10)
        .all()
    )

    return {
        "child_stats": child_stats,
        "recent_logs": recent_logs,
    }


def reports_data() -> dict:
    totals_rows = (
        db.session.query(
            Child.name,
            func.coalesce(func.sum(ActivityLog.reward_minutes_snapshot), 0).label("minutes"),
            func.count(ActivityLog.id).label("tasks"),
        )
        .outerjoin(ActivityLog, ActivityLog.child_id == Child.id)
        .group_by(Child.id)
        .order_by(Child.name)
        .all()
    )

    activity_rows = (
        db.session.query(Activity.name, func.count(ActivityLog.id).label("times"))
        .join(ActivityLog, ActivityLog.activity_id == Activity.id)
        .group_by(Activity.id)
        .order_by(func.count(ActivityLog.id).desc())
        .limit(10)
        .all()
    )

    start_week = datetime.combine(date.today() - timedelta(days=6), datetime.min.time())
    weekly_rows = (
        db.session.query(
            Child.name,
            func.coalesce(func.sum(ActivityLog.reward_minutes_snapshot), 0).label("minutes"),
        )
        .outerjoin(
            ActivityLog,
            (ActivityLog.child_id == Child.id) & (ActivityLog.performed_at >= start_week),
        )
        .group_by(Child.id)
        .order_by(Child.name)
        .all()
    )

    totals = [
        {"name": row.name, "minutes": int(row.minutes or 0), "tasks": int(row.tasks or 0)}
        for row in totals_rows
    ]
    activity_freq = [
        {"name": row.name, "times": int(row.times or 0)} for row in activity_rows
    ]
    weekly = [{"name": row.name, "minutes": int(row.minutes or 0)} for row in weekly_rows]

    return {
        "totals": totals,
        "activity_freq": activity_freq,
        "weekly": weekly,
    }
