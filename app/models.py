from datetime import datetime

from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Child(TimestampMixin, db.Model):
    __tablename__ = "children"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(20), default="blue", nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    activity_logs = db.relationship(
        "ActivityLog", back_populates="child", cascade="all, delete-orphan"
    )


class Activity(TimestampMixin, db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    reward_minutes = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    activity_logs = db.relationship(
        "ActivityLog", back_populates="activity", cascade="all, delete-orphan"
    )


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"), nullable=False)
    reward_minutes_snapshot = db.Column(db.Integer, nullable=False)
    performed_at = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    child = db.relationship("Child", back_populates="activity_logs")
    activity = db.relationship("Activity", back_populates="activity_logs")
