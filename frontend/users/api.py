# frontend/users/api.py

from nicegui import ui
from frontend.common.api import get, post, put, delete, set_token


# === Регистрация ===
async def register_user(username: str, email: str, password: str):
    payload = {"username": username, "email": email, "password": password}
    resp = await post("/users/register/", json=payload)

    if not resp:
        ui.notify("⚠️ Грешка при връзка със сървъра.", color="negative")
        return None

    if resp.status_code in (200, 201):
        ui.notify("✅ Регистрацията беше успешна!")
        return resp.json()

    try:
        detail = resp.json().get("detail", resp.text)
    except Exception:
        detail = resp.text
    ui.notify(f"⚠️ Неуспешна регистрация: {detail}", color="negative")
    return None


# === Вход / Логин ===
async def login_user(username: str, password: str):
    payload = {"username": username, "password": password}
    resp = await post("/users/login/", json=payload)

    if not resp:
        ui.notify("⚠️ Грешка при връзка със сървъра.", color="negative")
        return None

    if resp.status_code == 200:
        data = resp.json()
        token = data.get("access_token")
        if token:
            set_token(token)
            ui.notify("🔓 Успешен вход!")
        else:
            ui.notify("⚠️ Липсва токен в отговора на логина.", color="warning")
        return data

    try:
        detail = resp.json().get("detail", resp.text)
    except Exception:
        detail = resp.text
    ui.notify(f"⚠️ Грешка при вход: {detail}", color="negative")
    return None


# === Извличане на всички потребители ===
async def get_users():
    resp = await get("/users/")
    if not resp:
        ui.notify("⚠️ Няма връзка със сървъра.", color="negative")
        return []

    if resp.status_code == 200:
        return resp.json()

    ui.notify(f"⚠️ Неуспешно зареждане на списъка с потребители ({resp.status_code})", color="negative")
    return []


# === Актуализиране на потребител ===
async def update_user(user_id: int, data: dict):
    """Актуализира съществуващ потребител по ID."""
    resp = await put(f"/users/{user_id}", json=data)

    if not resp:
        ui.notify("⚠️ Грешка при свързване със сървъра.", color="negative")
        return None

    if resp.status_code == 200:
        ui.notify("📝 Потребителят е актуализиран успешно!")
        return resp.json()

    try:
        detail = resp.json().get("detail", resp.text)
    except Exception:
        detail = resp.text
    ui.notify(f"⚠️ Неуспешна актуализация: {detail}", color="negative")
    return None


# === Изтриване на потребител ===
async def delete_user(user_id: int):
    resp = await delete(f"/users/{user_id}")

    if not resp:
        ui.notify("⚠️ Грешка при връзка със сървъра.", color="negative")
        return None

    if resp.status_code == 200:
        ui.notify("🗑️ Потребителят беше изтрит успешно.")
        return resp

    ui.notify(f"⚠️ Неуспешно изтриване: {resp.text}", color="negative")
    return resp


# === Смяна на парола ===
async def change_password(user_id: int, old_password: str, new_password: str):
    payload = {"old_password": old_password, "new_password": new_password}
    resp = await put(f"/users/{user_id}/change-password", json=payload)

    if not resp:
        ui.notify("⚠️ Грешка при връзка със сървъра.", color="negative")
        return None

    if resp.status_code == 200:
        ui.notify("🔑 Паролата е променена успешно!")
        return resp

    try:
        detail = resp.json().get("detail", resp.text)
    except Exception:
        detail = resp.text
    ui.notify(f"⚠️ Неуспешна смяна на парола: {detail}", color="negative")
    return resp


# === Профил на текущия потребител ===
async def get_profile():
    resp = await get("/users/me")

    if not resp:
        ui.notify("⚠️ Грешка при връзка със сървъра.", color="negative")
        return None

    if resp.status_code == 200:
        return resp.json()

    ui.notify(f"⚠️ Неуспешно зареждане на профил ({resp.status_code})", color="negative")
    return None


# === Изход ===
async def logout_user():
    set_token(None)
    ui.notify("🚪 Излязохте от профила.")
