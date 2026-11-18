import json
import logging
from typing import Callable, Any, Awaitable
from redis.asyncio import Redis
from redis.exceptions import RedisError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


async def get_or_set(
        redis: Redis,
        key: str,
        ttl: int,
        loader: Callable[[], Awaitable[Any]]

) -> Any:
    try:
        cached = await redis.get(key)
        if cached is not None:
            return json.loads(cached)
    except RedisError as err:
        logger.warning("Error: %s", err)

    data = await loader()

    try:
        await redis.set(key, json.dumps(data), ex=ttl)
    except RedisError as err:
        logger.warning("Error: %s", err)
    return data


async def invalidate_all_books(redis: Redis) -> None:
    try:
       await redis.delete("books:all")
    except RedisError as err:
        logger.warning("Error while deleting: %s", err)


async def invalidate_book(redis: Redis, book_id: int) -> None:
    try:
       await redis.delete(f"books:all", f"book:{book_id}")
    except RedisError as err:
        logger.warning("Error while deleting one book: %s", err)