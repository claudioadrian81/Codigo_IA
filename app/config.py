import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SQLITE_PATH = BASE_DIR / "app.db"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
