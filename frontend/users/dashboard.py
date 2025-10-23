from nicegui import ui
from frontend.users.api import get_users, update_user, delete_user, change_password


async def show_dashboard():
    """Основна таблица с потребителите"""
    with ui.card().classes("p-8 flex flex-col gap-4 shadow-xl w-full max-w-5xl"):
        ui.label("📋 Управление на потребители").classes("text-xl font-bold")

        rows_container = ui.column().classes("gap-2")

        # --- функция за обновяване на таблицата ---
        async def refresh_rows():
            rows_container.clear()
            users = await get_users()
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
                            ui.button(
                                "✏️",
                                on_click=lambda u=user: edit_user_dialog(u)
                            ).props("flat dense round")
                            ui.button(
                                "🗑️",
                                on_click=lambda u=user: confirm_delete(u)
                            ).props("flat dense round color=red")
                            ui.button(
                                "🔑",
                                on_click=lambda u=user: show_change_password(u)
                            ).props("flat dense round color=blue")

        # --- редакция ---
        def edit_user_dialog(user):
            with ui.dialog() as dialog, ui.card():
                ui.label(f"Редакция на {user['username']}").classes("text-lg font-bold")
                username_input = ui.input("Потребителско име", value=user["username"])
                email_input = ui.input("Имейл", value=user["email"])
                role_input = ui.select(["user", "admin"], value=user.get("role", "user"), label="Роля")

                async def save():
                    data = {
                        "username": username_input.value,
                        "email": email_input.value,
                        "role": role_input.value,
                    }
                    response = await update_user(user["id"], data)
                    if response:
                        ui.notify("✅ Потребителят е обновен!")
                        await refresh_rows()
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

                async def confirm_action():
                    ok = await delete_user(user["id"])
                    if ok:
                        ui.notify("✅ Потребителят е изтрит!")
                        await refresh_rows()
                    else:
                        ui.notify("❌ Грешка при изтриване!")
                    confirm.close()

                with ui.row().classes("justify-end gap-4"):
                    ui.button("Откажи", on_click=confirm.close)
                    ui.button("🗑️ Изтрий", on_click=confirm_action).classes("bg-red-500 text-white")

            confirm.open()

        # --- смяна на парола ---
        def show_change_password(user):
            username = user["username"]

            with ui.dialog() as dialog, ui.card():
                ui.label(f"Смяна на парола за {username}").classes("text-xl font-bold")

                old_password = ui.input("Стара парола", password=True)
                new_password = ui.input("Нова парола", password=True)
                confirm_password = ui.input("Повтори новата парола", password=True)

                async def change_password_action():
                    if not old_password.value.strip():
                        ui.notify("⚠️ Въведете старата парола")
                        return
                    if new_password.value != confirm_password.value:
                        ui.notify("⚠️ Новата парола не съвпада с потвърждението")
                        return
                    if len(new_password.value.strip()) < 6:
                        ui.notify("⚠️ Паролата трябва да е поне 6 символа")
                        return

                    ok = await change_password(user["id"], old_password.value, new_password.value)
                    if ok:
                        ui.notify("✅ Паролата е променена успешно!")
                        dialog.close()
                    else:
                        ui.notify("❌ Грешка при промяна на паролата")

                with ui.row().classes("gap-4 justify-between"):
                    ui.button("Смени паролата", on_click=change_password_action).classes(
                        "bg-green-500 text-white px-4 py-1 rounded"
                    )
                    ui.button("Откажи", on_click=dialog.close).classes(
                        "bg-gray-300 px-4 py-1 rounded"
                    )

            dialog.open()

        await refresh_rows()
