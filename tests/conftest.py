import os
import tempfile
import importlib
import pytest

def _load_flask_app():
    """
    Tries common patterns:
    1) from app import create_app -> create_app()
    2) from app import app -> app
    3) from run import app -> app
    """
    # Prefer a throwaway SQLite DB for tests
    db_fd, db_path = tempfile.mkstemp()
    os.environ.setdefault("FLASK_ENV", "testing")
    os.environ.setdefault("SECRET_KEY", "test-secret")
    # If your app uses SQLALCHEMY_DATABASE_URI or DATABASE_URL, set both:
    os.environ.setdefault("SQLALCHEMY_DATABASE_URI", f"sqlite:///{db_path}")
    os.environ.setdefault("DATABASE_URL", f"sqlite:///{db_path}")

    try:
        app_pkg = importlib.import_module("app")
        if hasattr(app_pkg, "create_app"):
            app = app_pkg.create_app()
        elif hasattr(app_pkg, "app"):
            app = app_pkg.app
        else:
            raise ImportError("No create_app() or app in app package")
    except Exception:
        run_mod = importlib.import_module("run")
        if hasattr(run_mod, "create_app"):
            app = run_mod.create_app()
        else:
            app = getattr(run_mod, "app")

    return app, db_fd, db_path

@pytest.fixture
def client():
    app, db_fd, db_path = _load_flask_app()
    app.config["TESTING"] = True

    # If using Flask-SQLAlchemy, try to create tables for tests.
    try:
        from app.models import db  # type: ignore
        with app.app_context():
            db.create_all()
    except Exception:
        # If your app doesn't use SQLAlchemy or auto-migrations, ignore.
        pass

    with app.test_client() as client:
        yield client

    try:
        os.close(db_fd)
        os.remove(db_path)
    except Exception:
        pass
