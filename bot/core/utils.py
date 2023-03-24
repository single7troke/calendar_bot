import aiohttp
from aiogram.filters.callback_data import CallbackData
from core.config import Config

config = Config()


class GoogleEventCallback(CallbackData, prefix="id"):
    event_id: str


async def event_list():
    async with aiohttp.ClientSession() as session:
        url = f"{config.web_app_url}google-calendar/"
        async with session.get(url) as resp:
            data = await resp.json()
            return data


async def event_details(event_id: str):
    async with aiohttp.ClientSession() as session:
        url = f"{config.web_app_url}google-calendar/{event_id}"
        async with session.get(url) as resp:
            data = await resp.json()
            return data


async def get_user(user_id: str) -> bool:
    async with aiohttp.ClientSession() as session:
        url = f"{config.web_app_url}users/{user_id}"
        async with session.get(url) as resp:
            data = await resp.json()
            return data


async def get_all_users() -> dict:
    async with aiohttp.ClientSession() as session:
        url = f"{config.web_app_url}users/"
        async with session.get(url) as resp:
            data = await resp.json()
            return data


async def create_or_update_user(user_id: str, name: str, role: str = "user") -> bool:
    async with aiohttp.ClientSession() as session:
        url = f"{config.web_app_url}users/add_user"
        data = {"user_id": user_id, "role": role, "name": name}
        async with session.post(url, json=data) as resp:
            res = await resp.json()
            return res


async def delete_user(user_id: str) -> bool:
    async with aiohttp.ClientSession() as session:
        url = f"{config.web_app_url}users/delete"
        data = {"user_id": user_id}
        async with session.delete(url, json=data) as resp:
            res = await resp.json()
            return res
