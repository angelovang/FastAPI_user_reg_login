from nicegui import ui

from frontend.common import session
from frontend.common.api import _get_user_storage
from frontend.common.layout import add_header, add_subnav
from frontend.archaeology.dashboard_layers import show_layers_dashboard
from frontend.archaeology.dashboard_includes import show_layer_includes_dashboard
from frontend.archaeology.dashboard_fragments import show_fragments_dashboard
from frontend.archaeology.dashboard_pok import show_pok_dashboard
from frontend.archaeology.dashboard_ornaments import show_ornaments_dashboard
from frontend.common.session import get_session


# """Страница за управление на археологическите пластове"""
@ui.page('/layers')
def layers_page():
    # add_header()
    add_subnav()
    session = get_session()
    test = _get_user_storage()
    print(test, session)
    with ui.row().classes("items-center justify-center w-full p-4"):
        show_layers_dashboard()


# """Страница за управление на примеси"""
@ui.page('/layer_includes')
def includes_page():
    # add_header()
    add_subnav()
    with ui.row().classes("items-center justify-center w-full p-4"):
        show_layer_includes_dashboard()


# Страница за управление на фрагменти
@ui.page('/fragments')
def fragments_page():
    # add_header()
    add_subnav()
    with ui.row().classes("items-center justify-center w-full p-4"):
        show_fragments_dashboard()


# Страница за управление на ПОК
@ui.page('/pok')
def pok_page():
    # add_header()
    add_subnav()
    with ui.row().classes("items-center justify-center w-full p-4"):
        show_pok_dashboard()


# Страница за управление на орнаменти
@ui.page('/ornaments')
def ornaments_page():
    # add_header()
    add_subnav()
    with ui.row().classes("items-center justify-center w-full p-4"):
        show_ornaments_dashboard()