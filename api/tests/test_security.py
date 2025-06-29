from jwt import decode

from src.security.security import Settings, create_access_token


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)
    decoded = decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])
    assert decoded["test"] == data["test"]
    assert "exp" in decoded
