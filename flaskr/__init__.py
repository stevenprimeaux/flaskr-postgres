"""Initialize application."""

import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


def get_database_url():
    """Return database string in format required by SQLAlchemy."""
    return os.getenv("DATABASE_URL").replace(
        "postgres://",
        "postgresql://",
        1
    )


def get_secret_key():
    """Return secret key for session cookie."""
    return os.getenv("SECRET_KEY")


def create_app(test_config=None):
    """Define application factory."""
    from . import auth, blog

    app = Flask(__name__, instance_relative_config=True)

    if test_config is not None:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SECRET_KEY=get_secret_key(),
            SQLALCHEMY_DATABASE_URI=get_database_url()
        )

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    with app.app_context():
        db.create_all()

    app.add_url_rule("/", endpoint="index")

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
