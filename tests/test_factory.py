from flaskr import create_app, get_database_url, get_secret_key


def test_config():
    assert not create_app().testing
    assert create_app({
        "TESTING": True,
        "SECRET_KEY": get_secret_key(),
        "SQLALCHEMY_DATABASE_URI": get_database_url(),
    }).testing


def test_hello(client):
    response = client.get("/hello")
    assert response.data == b"Hello, World!"
