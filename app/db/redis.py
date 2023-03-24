import logging

from aioredis import Redis
from aioredis.exceptions import ConnectionError
from fastapi import Depends
from tenacity import retry, stop_after_delay, RetryCallState, retry_if_exception_type, wait_exponential, after_log

from db.abstract_cache import AbstractCache

logging.basicConfig(format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p %Z",
                    level=logging.INFO)
logger = logging.getLogger(__name__)
redis: Redis | None = None


async def get_redis() -> Redis:
    return redis


def no_connection(retry_state: RetryCallState):
    return ConnectionError


class RedisDB(AbstractCache):
    def __init__(self, client: Redis):
        self.redis = client

    @retry(retry=retry_if_exception_type(ConnectionError),
           wait=wait_exponential(),
           stop=stop_after_delay(15),
           after=after_log(logger, logging.INFO),
           retry_error_callback=no_connection)
    async def get(self, user_id: str):
        data = await self.redis.hgetall(name=user_id)
        return data

    @retry(retry=retry_if_exception_type(ConnectionError),
           wait=wait_exponential(),
           stop=stop_after_delay(15),
           after=after_log(logger, logging.INFO),
           retry_error_callback=no_connection)
    async def list(self):
        data = await self.redis.keys(pattern="*")
        return data

    @retry(retry=retry_if_exception_type(ConnectionError),
           wait=wait_exponential(),
           stop=stop_after_delay(15),
           after=after_log(logger, logging.INFO),
           retry_error_callback=no_connection)
    async def create_or_update(self, user_id: str, data: dict) -> None:
        data = await self.redis.hset(name=user_id, mapping=data)
        return data

    @retry(retry=retry_if_exception_type(ConnectionError),
           wait=wait_exponential(),
           stop=stop_after_delay(15),
           after=after_log(logger, logging.INFO),
           retry_error_callback=no_connection)
    async def delete(self, user_id: str) -> None:
        data = await self.redis.delete(user_id)
        return data


def get_redis_db(redis: Redis = Depends(get_redis)):
    return RedisDB(redis)
