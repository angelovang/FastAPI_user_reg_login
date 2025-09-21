# slot_test.py
from nicegui import ui

def test_table():
    table = ui.table(
        columns=[
            {'name': 'id', 'label': 'ID', 'field': 'id'},
            {'name': 'name', 'label': 'Name', 'field': 'name'},
            {'name': 'actions', 'label': 'Actions', 'field': 'id'},  # dummy field
        ],
        rows=[
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'},
        ],
        row_key='id'
    )

    # добавяме слот за колоната "actions"
    slot = table.add_slot('body-cell-actions', 'props')

    def actions_cell(props):
        with ui.row():
            ui.button(icon='edit', on_click=lambda: ui.notify(f"Edit {props.row['name']}"))
            ui.button(icon='delete', on_click=lambda: ui.notify(f"Delete {props.row['name']}"))

    slot.render = actions_cell


with ui.column().classes("p-8"):
    ui.label("Тестова таблица със слотове")
    test_table()

# стартираме на друг порт
ui.run(port=8082)
