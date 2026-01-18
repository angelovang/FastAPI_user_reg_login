from functools import wraps
from nicegui import ui, context

# глобална променлива за сесията - подлежи на обсъждане за сигурността
current_session = {}


# -------------------- Helper функции --------------------
def get_session():
    return current_session


def set_session(data: dict):
    global current_session
    current_session = data


def logout_action():
    global current_session
    current_session = {}
    ui.notify("✅ Излязохте успешно")
    ui.navigate.to("/")
