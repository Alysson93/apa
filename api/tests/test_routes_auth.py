from http import HTTPStatus


def test_login_token(client, user_db):
    response = client.post(
        "/auth/token",
        data={"username": user_db.username, "password": user_db.password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token
