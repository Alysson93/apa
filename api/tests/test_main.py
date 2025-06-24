from http import HTTPStatus


def test_root(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"msg": "Hello, World!"}


def test_user(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK
