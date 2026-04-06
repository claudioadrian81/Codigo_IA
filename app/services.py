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
    totals = (
        db.session.query(
            Child.name,
            func.coalesce(func.sum(ActivityLog.reward_minutes_snapshot), 0),
            func.count(ActivityLog.id),
        )
        .outerjoin(ActivityLog, ActivityLog.child_id == Child.id)
        .group_by(Child.id)
        .order_by(Child.name)
        .all()
    )

    activity_freq = (
        db.session.query(Activity.name, func.count(ActivityLog.id).label("times"))
        .join(ActivityLog, ActivityLog.activity_id == Activity.id)
        .group_by(Activity.id)
        .order_by(func.count(ActivityLog.id).desc())
        .limit(10)
        .all()
    )

    start_week = datetime.combine(date.today() - timedelta(days=6), datetime.min.time())
    weekly = (
        db.session.query(Child.name, func.coalesce(func.sum(ActivityLog.reward_minutes_snapshot), 0))
        .outerjoin(
            ActivityLog,
            (ActivityLog.child_id == Child.id) & (ActivityLog.performed_at >= start_week),
        )
        .group_by(Child.id)
        .order_by(Child.name)
        .all()
    )

    return {
        "totals": totals,
        "activity_freq": activity_freq,
        "weekly": weekly,
    }
