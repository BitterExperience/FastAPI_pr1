import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from pathlib import Path

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.user import UserModel
from app.security.password import hash_password

BASE_PATH = Path(__file__).resolve().parent.parent.parent


TEST_DATABASE_URL = f"sqlite+aiosqlite:///{BASE_PATH}/test_books.db"
test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture
async def test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(test_db):
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "user@example.com",
            "password": "secret123",
        }
    )
    assert response.status_code == 201
    user_data = response.json()
    user_data["password"] = "secret123"
    return user_data


@pytest.fixture
async def auth_client(client, test_user):
    response = client.post(
        "/users/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.fixture
async def create_author(auth_client):
    response = auth_client.post("/authors",

                json = {"name": "Лев Толстой",
                        "bio": " Русский классик"}
                )
    assert response.status_code == 201
    return response


@pytest.fixture
async def create_book(auth_client, create_author):
    assert create_author.status_code == 201
    author_id = create_author.json()["id"]
    response_create_book = auth_client.post(
        "/books", json={"title": "Война и мир", "author_id": author_id, "price": 1000.0}
    )
    assert response_create_book.status_code == 201
    return response_create_book


@pytest.fixture
async def admin_client(client, test_db):
    reg = client.post("/users/register",
            json={
                "username": "testadmin",
                "email": "testadmin@example.com",
                "password": "secret456"
        })
    assert reg.status_code == 201

    from app.crud.user import read_user_by_username_db, update_user_db
    async with TestSessionLocal() as session:
        user = await read_user_by_username_db("testadmin", session)
        await update_user_db(user, {"role": "admin"}, session)

    login = client.post(
        "/users/login",
        data={"username": "testadmin", "password": "secret456"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client