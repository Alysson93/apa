import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from src.main import app
from src.models.entities import User, table_registry
from src.repositories.UserRepository import UserRepository, get_user_repository
from src.security.hash import get_password_hash


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
def client(session):
    def override_user_repository():
        return UserRepository(session)

    app.dependency_overrides[get_user_repository] = override_user_repository
    yield TestClient(app)
    app.dependency_overrides.clear()


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


@pytest_asyncio.fixture
async def user_db(session):
    john = User(
        username="JohnDoe",
        password=get_password_hash("123456"),
        name="John",
        last_name="Doe",
        email="john@mail.com",
        phone="(00) 9 1234 - 5678",
        role="client",
    )
    jane = User(
        username="JaneDoe",
        password=get_password_hash("123456"),
        name="Jane",
        last_name="Doe",
        email="jane@mail.com",
        phone="(00) 9 1234 - 5678",
        role="client",
    )
    session.add_all([john, jane])
    await session.commit()
    await session.refresh(john)
    return john
