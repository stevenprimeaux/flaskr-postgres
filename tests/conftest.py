import os
import pytest

from sqlalchemy import text

from flaskr import create_app, db, get_database_url, get_secret_key

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": get_secret_key(),
        "SQLALCHEMY_DATABASE_URI": get_database_url(),
    })

    with app.app_context():
        db.session.execute(text(_data_sql))

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
