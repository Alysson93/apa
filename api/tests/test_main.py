from http import HTTPStatus


def test_root(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"msg": "Hello, World!"}


def test_create_user(client, user_request):
    response = client.post("/users", json=user_request)
    assert response.status_code == HTTPStatus.CREATED
    response = response.json()
    assert response['username'] == user_request['username']
    assert 'id' in response
    assert 'created_at' in response
    assert 'updated_at' in response


def test_user(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK
