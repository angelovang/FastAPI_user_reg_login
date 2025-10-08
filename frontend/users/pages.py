from nicegui import ui
from frontend.common.layout import add_header, add_subnav
from frontend.users.api import register_user, get_users, update_user, delete_user, change_password
from frontend.common.session import set_session
from frontend.common.api import async_request


@ui.page('/register')
def register_page():
    add_header()
    with ui.row().classes("items-center justify-center w-full"):
        with ui.card().classes("p-8 flex flex-col items-center gap-4 shadow-xl"):
            ui.label("Регистрация").classes("text-xl font-bold")
            username = ui.input("Потребителско име")
            email = ui.input("Имейл")
            password = ui.input("Парола", password=True)

            def validate_and_register():
                if len(username.value.strip()) < 3:
                    ui.notify("⚠️ Потребителското име трябва да е поне 3 символа")
                    return
                if "@" not in email.value or "." not in email.value:
                    ui.notify("⚠️ Въведете валиден имейл")
                    return
                if len(password.value.strip()) < 6:
                    ui.notify("⚠️ Паролата трябва да е поне 6 символа")
                    return
                response = register_user(username.value, email.value, password.value)
                if response and response.status_code == 200:
                    ui.notify("✅ Регистрация успешна!")
                    ui.navigate.to('/login')
                else:
                    ui.notify("❌ Грешка при регистрация!")

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
                response = await async_request("POST", "/users/login/", {
                    "username": username.value,
                    "password": password.value,
                })
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
                    ui.notify(f"✅ Успешно влязохте като {data['username']}!")
                    ui.navigate.to("/home")
                else:
                    ui.notify("❌ Невалидни данни за вход!", color="negative")

            ui.button("Влез", on_click=login_action)
            ui.button("⬅️ Назад", on_click=lambda: ui.navigate.to('/'))

@ui.page('/dashboard')
def dashboard_page():
    from frontend.users.dashboard import show_dashboard
    add_header()
    add_subnav()
    with ui.row().classes("items-center justify-center w-full p-8"):
        show_dashboard()
