import os
import pytest

from sqlalchemy import text

from flaskr import create_app, get_database_url, get_secret_key
from flaskr.models import db


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")
with open(os.path.join(os.path.dirname(__file__), "teardown.sql"), "rb") as f:
    _teardown_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": get_secret_key(),
        "SQLALCHEMY_DATABASE_URI": get_database_url(),
    })

    with app.app_context():
        db.session.execute(text(_data_sql))
        db.session.commit()

    yield app

    with app.app_context():
        db.session.execute(text(_teardown_sql))
        db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login",
            data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
