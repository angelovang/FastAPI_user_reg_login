# frontend/users/api.py
from nicegui import ui
from frontend.common.api import get, post, put, delete, set_token


# === Регистрация ===
async def register_user(username: str, email: str, password: str):
    payload = {"username": username, "email": email, "password": password}
    resp = await post("/users/", json=payload)

    if not resp:
        return None

    if resp.status_code in (200, 201):
        ui.notify("✅ Регистрацията беше успешна!")
        return resp.json()

    ui.notify(f"⚠️ Неуспешна регистрация: {resp.text}", color="negative")
    return None


# === Вход / Логин ===
async def login_user(username: str, password: str):
    payload = {"username": username, "password": password}
    resp = await post("/users/login/", json=payload)

    if not resp:
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

    ui.notify(f"⚠️ Грешка при вход: {resp.text}", color="negative")
    return None


# === Извличане на всички потребители ===
async def get_users():
    resp = await get("/users/")
    if not resp:
        return []

    if resp.status_code == 200:
        return resp.json()

    ui.notify("⚠️ Неуспешно зареждане на списъка с потребители.", color="negative")
    return []


# === Актуализиране на потребител ===
async def update_user(user_id: int, data: dict):
    resp = await put(f"/users/{user_id}", json=data)
    if not resp:
        return None

    if resp.status_code == 200:
        ui.notify("📝 Потребителят е актуализиран успешно!")
        return resp.json()

    ui.notify(f"⚠️ Неуспешна актуализация: {resp.text}", color="negative")
    return None


# === Изтриване на потребител ===
async def delete_user(user_id: int):
    resp = await delete(f"/users/{user_id}")
    if not resp:
        return False

    if resp.status_code == 200:
        ui.notify("🗑️ Потребителят беше изтрит успешно.")
        return True

    ui.notify(f"⚠️ Неуспешно изтриване: {resp.text}", color="negative")
    return False


# === Смяна на парола ===
async def change_password(old_password: str, new_password: str):
    payload = {"old_password": old_password, "new_password": new_password}
    resp = await put("/users/password/", json=payload)

    if not resp:
        return None

    if resp.status_code == 200:
        ui.notify("🔑 Паролата е променена успешно!")
        return True

    ui.notify(f"⚠️ Неуспешна смяна на парола: {resp.text}", color="negative")
    return False


# === Профил на текущия потребител ===
async def get_profile():
    resp = await get("/users/me")
    if not resp:
        return None

    if resp.status_code == 200:
        return resp.json()

    ui.notify("⚠️ Неуспешно зареждане на профил.", color="negative")
    return None


# === Изход ===
async def logout_user():
    set_token(None)
    ui.notify("🚪 Излязохте от профила.")
