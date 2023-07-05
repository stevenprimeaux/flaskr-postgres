from sqlalchemy import text
from werkzeug.security import check_password_hash

from flaskr.models import db


def test_index(client):
    # auth.login()
    response = client.get("/admin")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    response = client.get("/admin")
    assert b"test" in response.data
    assert b"other" in response.data
    assert b'href="/admin/1/update"' in response.data
    assert b'href="/admin/2/update"' in response.data


def test_update(client, app):
    # auth.login()
    assert client.get("/admin/3/update").status_code == 200
    client.post(
        "/admin/3/update", data={"password": "pw1"}
    )

    with app.app_context():
        user = db.session.execute(
            text("select * from users where id = 3;")
        ).fetchone()
        assert check_password_hash(user.password, "pw1")


def test_update_validate(client):
    # auth.login()
    response = client.post("/admin/3/update", data={"password": ""})
    assert b"Password is required." in response.data


def test_delete(client, app):
    # auth.login()
    response = client.post("/admin/3/delete")
    assert response.headers["Location"] == "/admin/"

    with app.app_context():
        user = db.session.execute(
            text("select * from users where id = 3;")
        ).fetchone()
        assert user is None
