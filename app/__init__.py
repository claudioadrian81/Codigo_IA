from flask import Flask

from .config import Config
from .extensions import db


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

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

    register_cli(app)
    register_error_handlers(app)

    return app


def register_cli(app: Flask) -> None:
    from .models import Activity, Child

    @app.cli.command("init-db")
    def init_db() -> None:
        """Inicializa la base de datos y carga datos de ejemplo."""
        db.drop_all()
        db.create_all()

        children = [Child(name="Ana"), Child(name="Sofía")]
        activities = [
            Activity(name="Ordenar el cuarto", reward_minutes=15, description="Dejar todo en orden"),
            Activity(name="Lavar los platos", reward_minutes=20),
            Activity(name="Barrer el piso", reward_minutes=15),
            Activity(name="Hacer la cama", reward_minutes=10),
            Activity(name="Guardar la ropa", reward_minutes=12),
            Activity(name="Limpiar la mesa", reward_minutes=8),
        ]

        db.session.add_all(children + activities)
        db.session.commit()
        print("Base de datos inicializada con datos de ejemplo.")


def register_error_handlers(app: Flask) -> None:
    from flask import render_template

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(_error):
        db.session.rollback()
        return render_template("errors/500.html"), 500
