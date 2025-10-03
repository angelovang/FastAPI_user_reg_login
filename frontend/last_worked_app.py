from nicegui import ui, app
import requests
import httpx

API_URL = "http://127.0.0.1:8000"
token = None

# глобална променлива за сесията - подлежи на обсъждане за сигурността
current_session = {}


# -------------------- Helper функции --------------------
def get_session():
    return current_session


# -------------------- Navbar --------------------
def add_header():
    with ui.element("div").classes(
            "fixed top-0 left-0 w-full h-16 bg-amber-100 shadow-md flex items-center justify-center z-50"
    ):
        ui.icon("museum").classes("text-stone-700 text-3xl")  # иконка (можеш да смениш с друга)
        ui.label("___Archaeological data entry system___").classes(
            "text-2xl font-serif italic text-stone-800"
        )
        ui.icon("history_edu").classes("text-stone-700 text-3xl")
    # оставяме празно място под navbar, за да не се застъпва със съдържанието
    ui.space().classes("h-9")


# ----------------- Допълнителен Navbar ---------------
def add_subnav():
    session = get_session()
    username = session.get("username", "гост")
    role = session.get("role", "user")

    with ui.row().classes(
            "w-full h-12 bg-amber-200 shadow flex items-center px-6 gap-6"
    ):
        ui.button("🏠 Home", on_click=lambda: ui.navigate.to("/home")).props("flat")

        ui.space()  # празно място от ляво

        ui.button("🪨 Пластове", on_click=lambda: ui.navigate.to("/layers")).props("flat")
        ui.button("⚗️ Примеси", on_click=lambda: ui.navigate.to("/layer_includes")).props("flat")
        ui.button("📐 ПОК", on_click=lambda: ui.navigate.to("/pok")).props("flat")
        ui.button("🧩 Фрагменти", on_click=lambda: ui.navigate.to("/fragments")).props("flat")
        ui.button("🎨 Орнаменти", on_click=lambda: ui.navigate.to("/ornaments")).props("flat")

        ui.space()  # празно място от дясно

        ui.label(f"🔑 Logged as: {username}").classes("text-sm italic")

        # 🔹 Показваме "Edit users" само за admin
        if role == "admin":
            ui.button("👥 Edit users", on_click=lambda: ui.navigate.to("/dashboard")).props("flat")

        ui.button("🚪 Logout", on_click=logout_action).props("flat")


# -------------------- API функции --------------------
def register(username, email, password):
    try:
        response = requests.post(f"{API_URL}/users/", json={
            "username": username,
            "email": email,
            "password": password
        })

        if response.status_code == 200:
            ui.notify("✅ Регистрация успешна!")
        else:
            ui.notify(f"❌ Грешка: {response.json().get('detail', 'Unknown error')}")

    except Exception as e:
        ui.notify(f"❌ Грешка при връзка с бекенда: {e}")


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


# -------------------- UI функции --------------------
def show_register():
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

            # ако всичко е ок → извикай backend API
            register(username.value, email.value, password.value)

        ui.button("Регистрирай", on_click=validate_and_register)
        ui.button("⬅️ Назад", on_click=lambda: ui.navigate.to('/'))


def show_login():
    global current_session
    with ui.card().classes("p-8 flex flex-col items-center gap-4 shadow-xl"):
        ui.label("Вход").classes("text-xl font-bold")
        username = ui.input("Потребителско име")
        password = ui.input("Парола", password=True)

        async def login_action():
            if len(username.value.strip()) < 3:
                ui.notify("⚠️ Потребителското име трябва да е поне 3 символа")
                return

            if len(password.value.strip()) < 4:
                ui.notify("⚠️ Паролата трябва да е поне 6 символа")
                return

            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        "http://localhost:8000/login/",
                        json={"username": username.value, "password": password.value},
                    )
                    if response.status_code == 200:
                        data = response.json()
                        # използваме сесия от клиента
                        session = ui.context.client.storage
                        session["token"] = data["access_token"]
                        session["token_type"] = data.get("token_type", "bearer")
                        session["username"] = data["username"]
                        session["id"] = data["id"]
                        session["role"] = data.get("role", "user")  # <--- добавено

                        global current_session
                        current_session = session  # Запомняме сесията в глобална променлива !

                        ui.notify(f"✅ Успешно влязохте като {data['username']}!")
                        ui.navigate.to("/home")
                    else:
                        ui.notify("❌ Невалидни данни за вход!", color="negative")

                except Exception as e:
                    ui.notify(f"⚠️ Грешка при връзка със сървъра: {e}", color="negative")

        ui.button("Влез", on_click=login_action)
        ui.button("⬅️ Назад", on_click=lambda: ui.navigate.to('/'))


def show_dashboard():
    session = ui.context.client.storage
    username = session.get("username", "гост")
    user_id = session.get("id")
    user_role = session.get("role", "user")

    with ui.card().classes("p-8 flex flex-col gap-4 shadow-xl w-full max-w-4xl"):
        ui.label(f"📋 Таблица потребители").classes("text-xl font-bold")

        rows_container = ui.column().classes("gap-2")

        # --- обновяване на редовете ---
        def refresh_rows():
            rows_container.clear()
            try:
                users = get_users()  # извиква backend-а
                for user in users:
                    with rows_container:
                        with ui.row().classes("items-center gap-4 border-b py-2"):
                            ui.label(str(user['id'])).classes("w-8")
                            ui.label(user['username']).classes("w-48")
                            ui.label(user['email']).classes("w-64")
                            ui.label(user['role']).classes("w-32")  # <-- ново поле
                            with ui.row().classes("gap-2"):
                                # Бутон за смяна на парола
                                ui.button("🔑",
                                          on_click=lambda u=user: show_change_password(u['id'], u['username'])).props(
                                    'flat dense round color=blue')
                                ui.button("✏️", on_click=lambda u=user: edit_user_dialog(u)).props(
                                    'flat dense round')
                                ui.button("🗑️", on_click=lambda u=user: confirm_delete(u)).props(
                                    'flat dense round color=red')

            except Exception as e:
                ui.notify(f"⚠️ Грешка при зареждане на потребители: {e}", color="negative")

        # --- редакция ---
        def edit_user_dialog(user):
            with ui.dialog() as dialog, ui.card():
                ui.label(f"Редакция на {user['username']}").classes("text-xl")
                username_input = ui.input("Потребителско име", value=user['username'])
                email_input = ui.input("Имейл", value=user['email'])
                role_input = ui.select(["user", "admin"], value=user.get('role', 'user'), label="Роля")  # <-- ново

                def save():
                    if update_user(user['id'], username_input.value, email_input.value, role_input.value):
                        ui.notify("✅ Потребителят е обновен!")
                        refresh_rows()
                    else:
                        ui.notify("❌ Грешка при обновяване!")
                    dialog.close()

                with ui.row().classes("gap-4 justify-between"):
                    ui.button("Запази", on_click=save).classes("bg-green-500 text-white px-4 py-1 rounded")
                    ui.button("Откажи", on_click=dialog.close).classes("bg-gray-300 px-4 py-1 rounded")

            dialog.open()

        # --- потвърждение на изтриване ---
        def confirm_delete(user):
            with ui.dialog() as confirm, ui.card():
                ui.label("Сигурни ли сте, че искате да изтриете този потребител?").classes("text-lg")
                with ui.row().classes("justify-end gap-4"):
                    ui.button("❌ Откажи", on_click=confirm.close)
                    ui.button("🗑️ Изтрий", on_click=lambda: (
                        delete_user_action(user), confirm.close()
                    )).classes("bg-red-500 text-white")

            confirm.open()

        # --- изтриване ---
        def delete_user_action(user):
            if delete_user(user['id']):
                ui.notify("✅ Потребителят е изтрит!")
                refresh_rows()
            else:
                ui.notify("❌ Грешка при изтриване!")

        # --- смяна на парола ---
        def show_change_password(user_id, username):
            with ui.dialog() as dialog, ui.card():
                ui.label(f"Смяна на парола за {username}").classes("text-xl font-bold")

                old_password = ui.input("Старa парола", password=True)
                new_password = ui.input("Нова парола", password=True)
                confirm_password = ui.input("Повтори новата парола", password=True)

                def change_password_action():
                    if new_password.value != confirm_password.value:
                        ui.notify("⚠️ Новата парола не съвпада с потвърждението")
                        return

                    if len(new_password.value.strip()) < 6:
                        ui.notify("⚠️ Паролата трябва да е поне 6 символа")
                        return

                    try:
                        response = requests.put(
                            f"{API_URL}/users/{user_id}/change-password",
                            json={
                                "old_password": old_password.value,
                                "new_password": new_password.value
                            }
                        )

                        if response.status_code == 200:
                            ui.notify("✅ Паролата е променена успешно!")
                            dialog.close()
                        else:
                            detail = response.json().get("detail", "Грешка")
                            ui.notify(f"❌ {detail}")

                    except Exception as e:
                        ui.notify(f"⚠️ Грешка при връзка с бекенда: {e}")

                with ui.row().classes("gap-4 justify-between"):
                    ui.button("Смени паролата", on_click=change_password_action).classes(
                        "bg-green-500 text-white px-4 py-1 rounded")
                    ui.button("Откажи", on_click=dialog.close).classes("bg-gray-300 px-4 py-1 rounded")

            dialog.open()

        refresh_rows()


# -------------------- Logout --------------------
def logout_action():
    # session = ui.context.client.storage
    # session.clear()
    global current_session
    current_session = {}
    ui.notify("✅ Излязохте успешно")
    ui.navigate.to("/")


# -------------------- Страници --------------------
@ui.page('/')
def main_page():
    add_header()
    with ui.row().classes("items-center justify-center w-full"):
        with ui.card().classes("p-8 flex flex-col items-center gap-4 shadow-xl"):
            ui.label("Добре дошли!").classes("text-3xl font-bold mb-4")
            ui.button("🔑 Вход", on_click=lambda: ui.navigate.to('/login')).classes("w-40")
            ui.button("📝 Регистрация", on_click=lambda: ui.navigate.to('/register')).classes("w-40")


@ui.page('/home')
def home_page():
    session = ui.context.client.storage
    add_header()
    add_subnav()
    with ui.column().classes("items-center justify-center w-full p-8"):
        ui.label("Добре дошли в системата за археологически данни!").classes("text-2xl font-bold")
        ui.label("Изберете модул от горното меню, за да продължите.").classes("text-lg italic text-gray-700")


@ui.page('/register')
def register_page():
    add_header()
    with ui.row().classes("items-center justify-center w-full"):
        show_register()


@ui.page('/login')
def login_page():
    add_header()
    with ui.row().classes("items-center justify-center w-full"):
        show_login()


@ui.page('/dashboard')
def dashboard_page():
    add_header()
    with ui.row().classes("items-center justify-center w-full"):
        show_dashboard()


# ------------------- Dummy старници ------------------
@ui.page('/layers')
def layers_page():
    add_header()
    add_subnav()
    with ui.column().classes("items-center justify-center p-8"):
        ui.label("🪨 Пластове").classes("text-2xl font-bold")
        ui.label("Тук ще бъде модулът за управление на пластовете.").classes("text-lg italic text-gray-700")


@ui.page('/layer_includes')
def includes_page():
    add_header()
    add_subnav()
    with ui.column().classes("items-center justify-center p-8"):
        ui.label("⚗️ Примеси").classes("text-2xl font-bold")
        ui.label("Тук ще бъде модулът за управление на примесите.").classes("text-lg italic text-gray-700")


@ui.page('/pok')
def pok_page():
    add_header()
    add_subnav()
    with ui.column().classes("items-center justify-center p-8"):
        ui.label("📐 ПОК").classes("text-2xl font-bold")
        ui.label("Тук ще бъде модулът за ПОК (по-късно ще се уточни функционалността).").classes(
            "text-lg italic text-gray-700")


@ui.page('/fragments')
def fragments_page():
    add_header()
    add_subnav()
    with ui.column().classes("items-center justify-center p-8"):
        ui.label("🧩 Фрагменти").classes("text-2xl font-bold")
        ui.label("Тук ще бъде модулът за управление на фрагментите.").classes("text-lg italic text-gray-700")


@ui.page('/ornaments')
def ornaments_page():
    add_header()
    add_subnav()
    with ui.column().classes("items-center justify-center p-8"):
        ui.label("🎨 Орнаменти").classes("text-2xl font-bold")
        ui.label("Тук ще бъде модулът за управление на орнаментите.").classes("text-lg italic text-gray-700")


# -------------------- Стартиране --------------------
ui.run(port=8081, storage_secret='private key')
