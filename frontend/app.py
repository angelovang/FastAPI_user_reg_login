from nicegui import ui
import requests
import httpx

API_URL = "http://127.0.0.1:8000"
token = None

# проста глобална променлива за демо
current_user = None

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
    ui.space().classes("h-20")


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


def update_user(user_id, username, email):
    try:
        response = requests.put(f"{API_URL}/users/{user_id}", json={
            "username": username,
            "email": email
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
        ui.button("Регистрирай", on_click=lambda: register(username.value, email.value, password.value))
        ui.button("⬅️ Назад", on_click=lambda: ui.navigate.to('/'))


'''
def show_login():
    with ui.card().classes("p-8 flex flex-col items-center gap-4 shadow-xl"):
        ui.label("Вход").classes("text-xl font-bold")
        username = ui.input("Потребителско име")
        password = ui.input("Парола", password=True)

        def login_action():
            global current_user
            try:
                response = requests.post("http://127.0.0.1:8000/login/", json={
                    "username": username.value,
                    "password": password.value,
                })
                if response.status_code == 200:
                    current_user = response.json()  # запазваме данните
                    ui.notify("✅ Успешно влязохте!")
                    ui.navigate.to('/dashboard')
                elif response.status_code == 401:
                    ui.notify("❌ Невалидно потребителско име или парола")
                else:
                    ui.notify(f"⚠️ Грешка при вход: {response.text}")
            except Exception as e:
                ui.notify(f"⚠️ Няма връзка със сървъра: {e}")

        ui.button("Влез", on_click=login_action)
        ui.button("⬅️ Назад", on_click=lambda: ui.navigate.to('/'))
'''

def show_login():
    with ui.card().classes("p-8 flex flex-col items-center gap-4 shadow-xl"):
        ui.label("Вход").classes("text-xl font-bold")
        username = ui.input("Потребителско име")
        password = ui.input("Парола", password=True)

        async def login_action():
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

                        ui.notify(f"✅ Успешно влязохте като {data['username']}!")
                        ui.navigate.to("/dashboard")
                    else:
                        ui.notify("❌ Невалидни данни за вход!", color="negative")
                except Exception as e:
                    ui.notify(f"⚠️ Грешка при връзка със сървъра: {e}", color="negative")

        ui.button("Влез", on_click=login_action)
        ui.button("⬅️ Назад", on_click=lambda: ui.navigate.to('/'))


'''
def show_dashboard():
    """Dashboard с отделни редове и бутони за всеки ред"""
    global current_user
    if not current_user:  # ако няма логнат
        ui.notify("⚠️ Трябва първо да влезете!")
        ui.navigate.to('/login')
        return

    with ui.card().classes("p-8 flex flex-col gap-4 shadow-xl w-full max-w-4xl"):
        ui.label(f"📋 Таблица потребители - Здравей, {current_user['username']} ! ").classes("text-xl font-bold")

        # Контейнер за редовете
        rows_container = ui.column().classes("gap-2")

        # --- Функция за обновяване на редовете ---
        def refresh_rows():
            rows_container.clear()
            users = get_users()  # взимаме актуалните данни
            for user in users:
                with rows_container:
                    with ui.row().classes("items-center gap-4 border-b py-2"):
                        ui.label(str(user['id'])).classes("w-8")
                        ui.label(user['username']).classes("w-48")
                        ui.label(user['email']).classes("w-64")
                        with ui.row().classes("gap-2"):
                            ui.button("✏️",on_click=lambda u=user: edit_user_dialog(u)).props(
                                'flat dense round')
                            ui.button("🗑️",on_click=lambda u=user: delete_user_action(u)).props(
                                'flat dense round color=red')

        # --- Диалог за редакция ---
        def edit_user_dialog(user):
            with ui.dialog() as dialog, ui.card():
                ui.label(f"Редакция на {user['username']}").classes("text-xl")
                username = ui.input("Потребителско име", value=user['username'])
                email = ui.input("Имейл", value=user['email'])

                def save():
                    if update_user(user['id'], username.value, email.value):
                        ui.notify("✅ Потребителят е обновен!")
                        refresh_rows()
                    else:
                        ui.notify("❌ Грешка при обновяване!")
                    dialog.close()

                def confirm_delete():
                    with ui.dialog() as confirm, ui.card().classes("p-4"):
                        ui.label(f"❗ Сигурни ли сте, че искате да изтриете '{user['username']}'?").classes(
                            "text-lg text-red-600"
                        )

                        def really_delete():
                            if delete_user(user['id']):
                                ui.notify("✅ Потребителят е изтрит!")
                                refresh_rows()
                            else:
                                ui.notify("❌ Грешка при изтриване!")
                            confirm.close()
                            dialog.close()

                        with ui.row().classes("gap-4 justify-end"):
                            ui.button("Да, изтрий", on_click=really_delete).classes(
                                "bg-red-500 text-white px-4 py-1 rounded"
                            )
                            ui.button("Откажи", on_click=confirm.close).classes(
                                "bg-gray-300 px-4 py-1 rounded"
                            )

                    confirm.open()

                with ui.row().classes("gap-4 justify-between"):
                    ui.button("Запази", on_click=save).classes("bg-green-500 text-white px-4 py-1 rounded")
                    ui.button("Изтрий", on_click=confirm_delete).classes("bg-red-500 text-white px-4 py-1 rounded")
                    ui.button("Откажи", on_click=dialog.close).classes("bg-gray-300 px-4 py-1 rounded")

            dialog.open()  # <-- важно: отваря диалога

        # --- Функция за изтриване с потвърждение ---
        def delete_user_action(user):
            with ui.dialog() as dialog, ui.card().classes("p-4"):
                ui.label(f"❗ Сигурни ли сте, че искате да изтриете '{user['username']}'?").classes(
                    "text-lg text-red-600"
                )

                def confirm_delete():
                    if delete_user(user['id']):
                        ui.notify("✅ Потребителят е изтрит!")
                        refresh_rows()
                    else:
                        ui.notify("❌ Грешка при изтриване!")
                    dialog.close()

                with ui.row().classes("gap-4 justify-end"):
                    ui.button("Да, изтрий", on_click=confirm_delete).classes("bg-red-500 text-white px-4 py-1 rounded")
                    ui.button("Откажи", on_click=dialog.close).classes("bg-gray-300 px-4 py-1 rounded")

            dialog.open()

        # --- Първоначално зареждане ---
        refresh_rows()
'''

def show_dashboard():
    session = ui.context.client.storage
    username = session.get("username", "гост")

    with ui.card().classes("p-8 flex flex-col gap-4 shadow-xl w-full max-w-4xl"):
        ui.label(f"📋 Табло потребители - Здравей, {username}!").classes("text-xl font-bold")

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
                            with ui.row().classes("gap-2"):
                                ui.button("✏️", on_click=lambda u=user: edit_user_dialog(u)).props(
                                    'flat dense round icon=edit')
                                ui.button("🗑️", on_click=lambda u=user: delete_user_action(u)).props(
                                    'flat dense round icon=delete color=red')
            except Exception as e:
                ui.notify(f"⚠️ Грешка при зареждане на потребители: {e}", color="negative")

        # --- редакция ---
        def edit_user_dialog(user):
            with ui.dialog() as dialog, ui.card():
                ui.label(f"Редакция на {user['username']}").classes("text-xl")
                username_input = ui.input("Потребителско име", value=user['username'])
                email_input = ui.input("Имейл", value=user['email'])

                def save():
                    if update_user(user['id'], username_input.value, email_input.value):
                        ui.notify("✅ Потребителят е обновен!")
                        refresh_rows()
                    else:
                        ui.notify("❌ Грешка при обновяване!")
                    dialog.close()

                def confirm_delete():
                    with ui.dialog() as confirm, ui.card():
                        ui.label("Сигурни ли сте, че искате да изтриете този потребител?").classes("text-lg")
                        with ui.row().classes("justify-end gap-4"):
                            ui.button("❌ Откажи", on_click=confirm.close)
                            ui.button("🗑️ Изтрий", on_click=lambda: (
                                delete_user_action(user), confirm.close(), dialog.close()
                            )).classes("bg-red-500 text-white")

                    confirm.open()

                with ui.row().classes("gap-4 justify-between"):
                    ui.button("Запази", on_click=save).classes("bg-green-500 text-white px-4 py-1 rounded")
                    ui.button("Изтрий", on_click=confirm_delete).classes("bg-red-500 text-white px-4 py-1 rounded")
                    ui.button("Откажи", on_click=dialog.close).classes("bg-gray-300 px-4 py-1 rounded")

            dialog.open()

        # --- изтриване ---
        def delete_user_action(user):
            if delete_user(user['id']):
                ui.notify("✅ Потребителят е изтрит!")
                refresh_rows()
            else:
                ui.notify("❌ Грешка при изтриване!")

        refresh_rows()

# -------------------- Страници --------------------
@ui.page('/')
def main_page():
    add_header()
    with ui.row().classes("items-center justify-center w-full"):
        with ui.card().classes("p-8 flex flex-col items-center gap-4 shadow-xl"):
            ui.label("Добре дошли!").classes("text-3xl font-bold mb-4")
            ui.button("🔑 Вход", on_click=lambda: ui.navigate.to('/login')).classes("w-40")
            ui.button("📝 Регистрация", on_click=lambda: ui.navigate.to('/register')).classes("w-40")


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


# -------------------- Стартиране --------------------
ui.run(port=8081)
