from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = "dev-secret-key-change-me"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'app.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
