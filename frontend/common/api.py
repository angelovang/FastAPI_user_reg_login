# frontend/common/api.py
import os
import httpx
import asyncio
from nicegui import ui

# === Конфигурация на API ===
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
TIMEOUT = float(os.getenv("API_TIMEOUT", "5.0"))


# === Безопасно съхранение на токена в сесията на NiceGUI ===
from nicegui import context

def _get_user_storage():
    """Безопасен достъп до session storage на текущия клиент в NiceGUI 3.x"""
    try:
        client = context.get_client()
        print("test!!!!!!!!!!!", client)
        if client and hasattr(client, 'storage'):
            return client.storage.user
    except Exception:
        pass
    # fallback за случаи без активна сесия (примерно при backend task)
    return {}

def set_token(token: str | None):
    """Запазва токена за текущия потребител (в сесията)."""
    storage = _get_user_storage()
    storage['token'] = token

def get_token() -> str | None:
    """Връща токена за текущия потребител."""
    storage = _get_user_storage()
    return storage.get('token')


# === Основна функция за асинхронни заявки ===
async def request(method: str, endpoint: str, **kwargs):
    """Централизирана HTTP заявка с JWT поддръжка и обработка на грешки."""
    url = f"{API_URL}{endpoint}"

    headers = kwargs.pop("headers", {})
    token = get_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.request(method, url, headers=headers, **kwargs)
            return response
        except httpx.RequestError as e:
            ui.notify(f"⚠️ Грешка при връзка с API: {e}", color="negative")
            return None


# === Удобни шорткъти ===
async def get(endpoint: str, **kwargs):
    return await request("GET", endpoint, **kwargs)

async def post(endpoint: str, **kwargs):
    return await request("POST", endpoint, **kwargs)

async def put(endpoint: str, **kwargs):
    return await request("PUT", endpoint, **kwargs)

async def delete(endpoint: str, **kwargs):
    return await request("DELETE", endpoint, **kwargs)


# === Съвместимост със стар код ===
async_request = request
