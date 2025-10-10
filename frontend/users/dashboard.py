# frontend/users/dashboard_layers.py

from nicegui import ui
import requests
from frontend.users.api import get_users, update_user, delete_user, change_password
'''
API_URL = "http://127.0.0.1:8000"


# -------------------- CRUD API функции --------------------
def get_users():
    try:
        response = requests.get(f"{API_URL}/users/")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        ui.notify(f"❌ Грешка при зареждане на потребителите: {e}")
    return []


def update_user(user_id, username, email, role):
    try:
        response = requests.put(f"{API_URL}/users/{user_id}", json={
            "username": username,
            "email": email,
            "role": role
        })
        return response.status_code == 200
    except Exception as e:
        ui.notify(f"❌ Грешка при обновяване: {e}")
        return False


def delete_user(user_id):
    try:
        response = requests.delete(f"{API_URL}/users/{user_id}")
        return response.status_code == 200
    except Exception as e:
        ui.notify(f"❌ Грешка при изтриване: {e}")
        return False
'''
from nicegui import ui
from frontend.users.api import get_users, update_user, delete_user, change_password


def show_dashboard():
    """Основна таблица с потребителите"""
    with ui.card().classes("p-8 flex flex-col gap-4 shadow-xl w-full max-w-5xl"):
        ui.label("📋 Управление на потребители").classes("text-xl font-bold")

        rows_container = ui.column().classes("gap-2")

        # --- функция за обновяване на таблицата ---
        def refresh_rows():
            rows_container.clear()
            users = get_users()
            if not users:
                ui.label("⚠️ Няма намерени потребители.").classes("text-red-500 italic")
                return

            for user in users:
                with rows_container:
                    with ui.row().classes("items-center gap-4 border-b py-2"):
                        ui.label(str(user["id"])).classes("w-8")
                        ui.label(user["username"]).classes("w-48")
                        ui.label(user["email"]).classes("w-64")
                        ui.label(user["role"]).classes("w-32")
                        with ui.row().classes("gap-2"):
                            ui.button("✏️", on_click=lambda u=user: edit_user_dialog(u)).props("flat dense round")
                            ui.button("🗑️", on_click=lambda u=user: confirm_delete(u)).props(
                                "flat dense round color=red")
                            ui.button("🔑", on_click=lambda u=user: show_change_password(u)).props(
                                "flat dense round color=blue")

        # --- редакция ---
        def edit_user_dialog(user):
            with ui.dialog() as dialog, ui.card():
                ui.label(f"Редакция на {user['username']}").classes("text-lg font-bold")
                username_input = ui.input("Потребителско име", value=user["username"])
                email_input = ui.input("Имейл", value=user["email"])
                role_input = ui.select(["user", "admin"], value=user.get("role", "user"), label="Роля")

                def save():
                    if update_user(user["id"], username_input.value, email_input.value, role_input.value):
                        ui.notify("✅ Потребителят е обновен!")
                        refresh_rows()
                    else:
                        ui.notify("❌ Грешка при обновяване!")
                    dialog.close()

                with ui.row().classes("gap-4 justify-between"):
                    ui.button("💾 Запази", on_click=save).classes("bg-green-500 text-white")
                    ui.button("❌ Откажи", on_click=dialog.close)
            dialog.open()

        # --- потвърждение за изтриване ---
        def confirm_delete(user):
            with ui.dialog() as confirm, ui.card():
                ui.label(f"Изтриване на {user['username']}?").classes("text-lg")
                with ui.row().classes("justify-end gap-4"):
                    ui.button("Откажи", on_click=confirm.close)
                    ui.button("🗑️ Изтрий", on_click=lambda: (
                        delete_user_action(user),
                        confirm.close()
                    )).classes("bg-red-500 text-white")
            confirm.open()

        def delete_user_action(user):
            if delete_user(user["id"]):
                ui.notify("✅ Потребителят е изтрит!")
                refresh_rows()
            else:
                ui.notify("❌ Грешка при изтриване!")

        # --- смяна на парола ---
        def show_change_password(user):
            username = user["username"]
            user_id = user["id"]

            with ui.dialog() as dialog, ui.card():
                ui.label(f"Смяна на парола за {username}").classes("text-xl font-bold")

                old_password = ui.input("Стара парола", password=True)
                new_password = ui.input("Нова парола", password=True)
                confirm_password = ui.input("Повтори новата парола", password=True)

                def change_password_action():
                    if not old_password.value.strip():
                        ui.notify("⚠️ Въведете старата парола")
                        return

                    if new_password.value != confirm_password.value:
                        ui.notify("⚠️ Новата парола не съвпада с потвърждението")
                        return

                    if len(new_password.value.strip()) < 6:
                        ui.notify("⚠️ Паролата трябва да е поне 6 символа")
                        return

                    response = change_password(
                        user["id"],
                        old_password.value,
                        new_password.value
                    )

                    if response is None:
                        ui.notify("❌ Няма връзка със сървъра или възникна грешка при заявката")
                        return

                    # Покажи статуса за по-добра диагностика
                    if response.status_code == 200:
                        ui.notify("✅ Паролата е променена успешно!")
                        dialog.close()
                    else:
                        try:
                            detail = response.json().get("detail", f"Грешка ({response.status_code})")
                        except Exception:
                            detail = f"⚠️ Неочакван отговор от сървъра: {response.text}"
                        ui.notify(f"❌ {detail}")

                with ui.row().classes("gap-4 justify-between"):
                    ui.button("Смени паролата", on_click=change_password_action).classes(
                        "bg-green-500 text-white px-4 py-1 rounded"
                    )
                    ui.button("Откажи", on_click=dialog.close).classes(
                        "bg-gray-300 px-4 py-1 rounded"
                    )

            dialog.open()

        refresh_rows()
