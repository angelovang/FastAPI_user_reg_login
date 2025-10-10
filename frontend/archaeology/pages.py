from nicegui import ui
from frontend.common.layout import add_header, add_subnav
from frontend.archaeology.dashboard_layers import show_layers_dashboard
from frontend.archaeology.dashboard_includes import show_layer_includes_dashboard

# """Страница за управление на археологическите пластове"""
@ui.page('/layers')
def layers_page():
    add_header()
    add_subnav()
    with ui.row().classes("items-center justify-center w-full p-4"):
        show_layers_dashboard()

# """Страница за управление на примеси"""
@ui.page('/layer_includes')
def includes_page():
    add_header()
    add_subnav()
    with ui.row().classes("items-center justify-center w-full p-4"):
        show_layer_includes_dashboard()


# 🧱 Dummy страници за останалите подмодули (остават временно)

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
