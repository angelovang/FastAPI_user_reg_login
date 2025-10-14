from nicegui import ui
from frontend.common.layout import add_header, add_subnav
from frontend.users.pages import register_page, login_page  # регистрират страниците
from frontend.archaeology.pages import *
from frontend.users.dashboard import show_dashboard



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
    add_header()
    add_subnav()
    with ui.column().classes("items-center justify-center w-full p-8"):
        ui.label("Добре дошли в системата за археологически данни!").classes("text-2xl font-bold")
        ui.label("Изберете модул от горното меню, за да продължите.").classes("text-lg italic text-gray-700")


ui.run(port=8081, storage_secret='private key', title='ADES')
