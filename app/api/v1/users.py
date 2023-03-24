from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from aioredis.exceptions import ConnectionError

from db.redis import get_redis_db, RedisDB
from models.models import BasicUser, CreateUser

router = APIRouter()


@router.get("/{user_id}", description="Return user's role if user exists, else False")
async def get_user(user_id: str, cache: RedisDB = Depends(get_redis_db)):
    data = await cache.get(user_id=user_id)

    if data == ConnectionError:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="redis connection error")

    return data


@router.get("/exist/{user_id}", description="Return True if user exists, else False")
async def is_user_exist(user_id: str, cache: RedisDB = Depends(get_redis_db)):
    data = await cache.exist(user_id)

    if data == ConnectionError:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="redis connection error")

    return True if data else False


@router.get("/", description="Return all users id from db")
async def get_all_users(cache: RedisDB = Depends(get_redis_db)):
    data = await cache.list()

    if data == ConnectionError:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="redis connection error")

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No any user in DB")

    return {"users_id": data}


@router.post("/add_user", description="Add new user into db")
async def create_or_update_user(user: CreateUser, cache: RedisDB = Depends(get_redis_db)):
    data = await cache.create_or_update(
        user_id=user.user_id,
        data={"role": user.role, "name": user.name})

    if data == ConnectionError:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="redis connection error")

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User wasn't created or updated")

    return data


@router.delete("/delete", description="Delete user from db")
async def delete_user(data: BasicUser, cache: RedisDB = Depends(get_redis_db)):
    user_id = data.user_id
    data = await cache.delete(user_id=user_id)

    if data == ConnectionError:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="redis connection error")

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User wasn't deleted")

    return data
