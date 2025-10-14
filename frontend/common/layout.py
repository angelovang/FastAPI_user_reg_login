from nicegui import ui
from frontend.common.session import get_session, logout_action


# -------------------- Navbar --------------------
def add_header():
    with ui.element("div").classes(
            "fixed top-0 left-0 w-full h-16 bg-amber-100 shadow-md flex items-center justify-center z-50"
    ):
        ui.icon("museum").classes("text-stone-700 text-3xl")
        ui.label("___Archaeological data entry system___").classes(
            "text-2xl font-serif italic text-stone-800"
        )
        ui.icon("history_edu").classes("text-stone-700 text-3xl")
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

        ui.button("⛏️ Пластове", on_click=lambda: ui.navigate.to("/layers")).props("flat")
        ui.button("⛰️ Примеси", on_click=lambda: ui.navigate.to("/layer_includes")).props("flat")
        ui.button("📐 ПОК", on_click=lambda: ui.navigate.to("/pok")).props("flat")
        ui.button("🧩 Фрагменти", on_click=lambda: ui.navigate.to("/fragments")).props("flat")
        ui.button("🌈 Орнаменти", on_click=lambda: ui.navigate.to("/ornaments")).props("flat")

        ui.space()  # празно място от дясно

        ui.label(f"🔑 Logged as: {username}").classes("text-sm italic")

        if role == "admin":
            ui.button("👥 Edit users", on_click=lambda: ui.navigate.to("/dashboard")).props("flat")

        ui.button("🚪 Logout", on_click=logout_action).props("flat")
