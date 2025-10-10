import httpx
import requests
from nicegui import ui

API_URL = "http://127.0.0.1:8000"


async def async_request(method: str, endpoint: str, json: dict = None):
    url = f"{API_URL}{endpoint}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, json=json)
            return response
        except Exception as e:
            ui.notify(f"⚠️ Грешка при връзка с бекенда: {e}", color="negative")
            return None


def sync_request(method: str, endpoint: str, json: dict = None):
    url = f"{API_URL}{endpoint}"
    try:
        response = requests.request(method, url, json=json)
        print(response)
        return response
    except Exception as e:
        ui.notify(f"⚠️ Грешка при връзка с бекенда: {e}", color="negative")
        return None
