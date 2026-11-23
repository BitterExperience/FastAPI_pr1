from redis.exceptions import RedisError
from sqlalchemy import delete
from app.models.book import BookModel
import pytest_asyncio

async def test_cache_hit(create_author, create_book, auth_client, fake_redis,
                         test_db
                         ):
    assert create_author.status_code == 201
    assert create_book.status_code == 201
    response1 = auth_client.get("/books")
    assert response1.status_code == 200
    cached1 = await fake_redis.get("books:all")
    print("response1", response1.json())
    print("cached1", cached1)
    print(len(response1.json()))
    await test_db.execute(delete(BookModel))
    await test_db.commit()
    response2 = auth_client.get("/books")
    assert response2.status_code == 200
    cached2 = await fake_redis.get("books:all")
    print(len(response2.json()))
    print("response2", response2.json())
    print("cache2", cached2)


async def test_cache_invalidation(client, fake_redis, test_db, create_author, create_book):
    assert create_author.status_code == 201
    assert create_book.status_code == 201
    response = client.get("books")
    assert response.status_code == 200
    cache = await fake_redis.get("books:all")
    assert cache is not None
    id_author = create_author.json()["id"]
    print("cache", cache)
    new_post = client.post("/books", json={"title": "New_book",
                                           "author_id": id_author,
                                           "price": 350
                                           })
    assert new_post.status_code == 201
    cache_none = await fake_redis.get("books:all")
    print(cache_none)
    assert cache_none is None





async def test_cache_fallback(client, fake_redis, create_author, create_book, monkeypatch):
    assert create_author.status_code == 201
    assert create_book.status_code == 201

    async def async_raise(*args, **kwargs):
        raise RedisError("Error redis")

    monkeypatch.setattr(fake_redis, "get", async_raise)

    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1