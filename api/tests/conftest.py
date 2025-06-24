import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import pytest_asyncio
from fastapi.testclient import TestClient

from src.main import app

# def pytest_configure():
#     os.environ["ENV"] = "test"

@pytest_asyncio.fixture
def client():
    return TestClient(app)


@pytest_asyncio.fixture
def user_request():
    return {
        "username": "JohnDoe",
        "password": "123456",
        "name": "John",
        "last_name": "Doe",
        "email": "john@mail.com",
        "phone": "(00) 9 1234 - 5678",
        "role": "client",
    }
