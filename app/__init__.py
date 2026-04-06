from pathlib import Path

from flask import Flask

from .config import Config
from .extensions import db


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    from .routes.activities import activities_bp
    from .routes.children import children_bp
    from .routes.dashboard import dashboard_bp
    from .routes.logs import logs_bp
    from .routes.reports import reports_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(children_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(reports_bp)

    initialize_database(app)
    register_error_handlers(app)

    return app


def initialize_database(app: Flask) -> None:
    """Crea las tablas y carga datos iniciales al iniciar la app."""
    from .models import Activity, Child

    with app.app_context():
        db.create_all()

        if Child.query.count() == 0:
            db.session.add_all([Child(name="Ana"), Child(name="Sofía")])

        if Activity.query.count() == 0:
            db.session.add_all(
                [
                    Activity(
                        name="Ordenar el cuarto",
                        reward_minutes=15,
                        description="Dejar todo en orden",
                    ),
                    Activity(name="Lavar los platos", reward_minutes=20),
                    Activity(name="Barrer el piso", reward_minutes=15),
                    Activity(name="Hacer la cama", reward_minutes=10),
                    Activity(name="Guardar la ropa", reward_minutes=12),
                    Activity(name="Limpiar la mesa", reward_minutes=8),
                ]
            )

        db.session.commit()


def register_error_handlers(app: Flask) -> None:
    from flask import render_template

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(_error):
        db.session.rollback()
        return render_template("errors/500.html"), 500
