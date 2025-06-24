import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import pytest_asyncio
from fastapi.testclient import TestClient

from src.main import app


@pytest_asyncio.fixture
def client():
    return TestClient(app)
