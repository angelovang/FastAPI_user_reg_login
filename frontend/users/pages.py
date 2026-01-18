from nicegui import ui
from frontend.common.layout import add_header, add_subnav
from frontend.users.api import register_user, get_users, update_user, delete_user, change_password
from frontend.common.session import set_session
from frontend.common.api import async_request, _get_user_storage


@ui.page('/register')
def register_page():
    add_header()
    with ui.row().classes("items-center justify-center w-full"):
        with ui.card().classes("p-8 flex flex-col items-center gap-4 shadow-xl"):
            ui.label("Регистрация").classes("text-xl font-bold")
            username = ui.input("Потребителско име")
            email = ui.input("Имейл")
            password = ui.input("Парола", password=True)

            async def validate_and_register():
                """Асинхронна функция за валидиране и регистрация."""
                if len(username.value.strip()) < 3:
                    ui.notify("⚠️ Потребителското име трябва да е поне 3 символа", color="warning")
                    return
                if "@" not in email.value or "." not in email.value:
                    ui.notify("⚠️ Въведете валиден имейл", color="warning")
                    return
                if len(password.value.strip()) < 6:
                    ui.notify("⚠️ Паролата трябва да е поне 6 символа", color="warning")
                    return

                # Асинхронна заявка към backend-а
                payload = {
                    "username": username.value.strip(),
                    "email": email.value.strip(),
                    "password": password.value.strip(),
                }

                try:
                    response = await async_request("POST", "/users/", json=payload)
                    if response and response.status_code == 200:
                        ui.notify("✅ Регистрация успешна!", color="positive")
                        ui.navigate.to('/login')
                    else:
                        detail = response.text if response else "Няма отговор"
                        ui.notify(f"❌ Грешка при регистрация: {detail}", color="negative")
                except Exception as e:
                    ui.notify(f"⚠️ Грешка при заявката: {e}", color="negative")

            ui.button("Регистрирай", on_click=validate_and_register)
            ui.button("⬅️ Назад", on_click=lambda: ui.navigate.to('/'))


@ui.page('/login')
def login_page():
    add_header()
    with ui.row().classes("items-center justify-center w-full"):
        with ui.card().classes("p-8 flex flex-col items-center gap-4 shadow-xl"):
            ui.label("Вход").classes("text-xl font-bold")
            username = ui.input("Потребителско име")
            password = ui.input("Парола", password=True)

            async def login_action():
                """Асинхронен вход на потребителя."""
                user_data = {
                    "username": getattr(username, "value", "").strip(),
                    "password": getattr(password, "value", "").strip(),
                }

                try:
                    response = await async_request("POST", "/users/login/", json=user_data)
                    if response and response.status_code == 200:
                        data = response.json()
                        session = {
                            "token": data["access_token"],
                            "token_type": data.get("token_type", "bearer"),
                            "username": data["username"],
                            "id": data["id"],
                            "role": data.get("role", "user")
                        }
                        set_session(session)
                        ui.notify(f"✅ Успешно влязохте като {data['username']}!", color="positive")
                        ui.navigate.to("/home")
                    else:
                        detail = response.text if response else "Няма отговор"
                        ui.notify(f"❌ Невалидни данни за вход ({detail})", color="negative")
                except Exception as e:
                    ui.notify(f"⚠️ Грешка при заявката: {e}", color="negative")

            ui.button("Влез", on_click=login_action)
            ui.button("⬅️ Назад", on_click=lambda: ui.navigate.to('/'))


@ui.page('/dashboard')
async def dashboard_page():
    """Потребителско табло."""
    from frontend.users.dashboard import show_dashboard
    add_header()
    add_subnav()
    with ui.row().classes("items-center justify-center w-full p-8"):
        await show_dashboard()
