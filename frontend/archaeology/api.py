# frontend/archaeology/api.py
import requests
from frontend.common.api import sync_request
from frontend.common.api import sync_request


API_URL = "http://127.0.0.1:8000/archaeology"

# ------------- Layers --------------

def get_layers():
    try:
        response = requests.get(f"{API_URL}/layers/")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"❌ Грешка при зареждане на пластове: {e}")
    return []

def create_layer(data: dict):
    try:
        response = requests.post(f"{API_URL}/layers/", json=data)
        return response
    except Exception as e:
        print(f"❌ Грешка при създаване на пласт: {e}")
        return None

def update_layer(layerid: int, data: dict):
    try:
        response = requests.put(f"{API_URL}/layers/{layerid}", json=data)
        return response
    except Exception as e:
        print(f"❌ Грешка при обновяване на пласт: {e}")
        return None

def delete_layer(layerid: int):
    try:
        response = requests.delete(f"{API_URL}/layers/{layerid}")
        return response
    except Exception as e:
        print(f"❌ Грешка при изтриване на пласт: {e}")
        return None


# -------------- Includes ---------------

def get_layer_includes():
    try:
        response = requests.get(f"{API_URL}/layer_includes/")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Грешка при зареждане на примеси: {e}")
        return []

def create_layer_include(data):
    try:
        response = requests.post(f"{API_URL}/layer_includes/", json=data)
        return response
    except Exception as e:
        print(f"Грешка при създаване на примес: {e}")
        return None

def update_layer_include(includeid, data):
    try:
        response = requests.put(f"{API_URL}/layer_includes/{includeid}", json=data)
        return response
    except Exception as e:
        print(f"Грешка при обновяване на примес: {e}")
        return None

def delete_layer_include(includeid):
    try:
        response = requests.delete(f"{API_URL}layer_includes/{includeid}")
        return response
    except Exception as e:
        print(f"Грешка при изтриване на примес: {e}")
        return None

