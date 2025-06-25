from http import HTTPStatus


def test_root(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"msg": "Hello, World!"}


def test_create_user(client, user_request):
    response = client.post("/users", json=user_request)
    assert response.status_code == HTTPStatus.CREATED
    response = response.json()
    assert response["username"] == user_request["username"]
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response


def test_create_user_already_exists(client, user_request, user_db):
    response = client.post("/users", json=user_request)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    response = client.get("/users")
    assert len(response.json()) == 0
    assert response.status_code == HTTPStatus.OK
