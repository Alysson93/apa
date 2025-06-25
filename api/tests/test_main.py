from http import HTTPStatus


def test_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'msg': 'Hello, World!'}


def test_create_user(client, user_request):
    response = client.post('/users', json=user_request)
    assert response.status_code == HTTPStatus.CREATED
    response = response.json()
    assert response['username'] == user_request['username']
    assert 'id' in response
    assert 'password' not in response
    assert response['created_at'] == response['updated_at']


def test_do_not_create_user_if_already_exists(client, user_request, user_db):
    response = client.post('/users', json=user_request)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client, user_db):
    response = client.get('/users')
    assert len(response.json()) == 2
    assert response.status_code == HTTPStatus.OK


def test_read_users_empty(client):
    response = client.get('/users')
    assert len(response.json()) == 0
    assert response.status_code == HTTPStatus.OK


def test_read_user(client, user_db):
    response = client.get(f'/users/{user_db.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == user_db.username


def test_read_user_not_found(client):
    response = client.get('/users/d1b1bb03-c32b-42cd-ae9e-f7ceb5bf4f43')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user_db, user_request):
    user_request['username'] = 'WaltMit'
    user_request['email'] = 'walt@mail.com'
    response = client.put(f'/users/{user_db.id}', json=user_request)
    assert response.status_code == HTTPStatus.OK
    response = response.json()
    assert response['username'] == 'WaltMit'
    assert response['created_at'] != response['updated_at']


def test_update_user_not_found(client, user_request):
    response = client.put(
        '/users/d1b1bb03-c32b-42cd-ae9e-f7ceb5bf4f43', json=user_request
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_do_not_update_user_with_already_used_username(
    client, user_db, user_request
):
    user_request['username'] = 'JaneDoe'
    response = client.put(f'/users/{user_db.id}', json=user_request)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_do_not_update_user_with_already_used_email(
    client, user_db, user_request
):
    user_request['email'] = 'jane@mail.com'
    response = client.put(f'/users/{user_db.id}', json=user_request)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_user(client, user_db):
    response = client.delete(f'/users/{user_db.id}')
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_not_found(client):
    response = client.delete('/users/d1b1bb03-c32b-42cd-ae9e-f7ceb5bf4f43')
    assert response.status_code == HTTPStatus.NOT_FOUND
