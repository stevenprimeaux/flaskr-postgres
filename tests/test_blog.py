import pytest

from sqlalchemy import text

from flaskr.models import db


def test_index(client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"Log Out" in response.data
    assert b"test title" in response.data
    assert b"by test on 2023-01-01" in response.data
    assert b"test\nbody" in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize("path", (
    "/create",
    "/1/update",
    "/1/delete",
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db.session.execute(
            text("update posts set author_id = 2 where id = 1;")
        )
        db.session.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize("path", (
    "/2/update",
    "/2/delete",
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post(
        "/create", data={"title": "title created", "body": "body created"}
    )

    with app.app_context():
        count = db.session.execute(
            text("select count(id) from posts;")
        ).fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post(
        "/1/update", data={"title": "title updated", "body": "body updated"}
    )

    with app.app_context():
        post = db.session.execute(
            text("select * from posts where id = 1;")
        ).fetchone()
        assert post.title == "title updated"
        assert post.body == "body updated"


@pytest.mark.parametrize("path", (
    "/create",
    "/1/update",
))
def test_create_update_validate(client, auth, path):
    auth.login()

    response = client.post(path, data={"title": "", "body": ""})
    assert b"Title is required." in response.data

    response = client.post(path, data={"title": "title", "body": ""})
    assert b"Body is required." in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    with app.app_context():
        post = db.session.execute(
            text("select * from posts where id = 1;")
        ).fetchone()
        assert post is None
