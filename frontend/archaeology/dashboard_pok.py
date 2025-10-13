from nicegui import ui
from datetime import date
from frontend.archaeology.api import (
    get_pok,
    create_pok,
    update_pok,
    delete_pok,
    get_layers,   # 🆕 за dropdown избор на локация
)

def show_pok_dashboard():
    """Главен панел за управление на таблица tblpok"""

    # --- Полета и преводи ---
    field_labels = {
        "pokid": "ID",
        "locationid": "Локация ID",
        "type": "Тип",
        "quantity": "Количество",
        "weight": "Тегло (гр.)",
        "sok_weight": "Сок тегло (гр.)",
        "recordenteredon": "Въведен на",
    }

    table_container = ui.column().classes("w-full")

    # 🆕 Зареждане на локациите за dropdown
    layers = get_layers() or []
    layers_options = {str(l["layerid"]): f"{l['layerid']} – {l.get('layername', '')}" for l in layers}

    # === 🟢 Нов запис ===
    def open_create_dialog():
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-2xl p-6"):
            ui.label("➕ Нов POK запис").classes("text-lg font-bold mb-2")

            with ui.grid(columns=2).classes("gap-4"):
                # locationid = ui.input("Локация ID").props("type=number")
                # 🆕 dropdown вместо input
                selected_layer = ui.select(options=layers_options, label="Локация")

                type_field = ui.input("Тип")
                quantity = ui.input("Количество").props("type=number")
                weight = ui.input("Тегло (гр.)").props("type=number step=0.001")
                sok_weight = ui.input("Сок тегло (гр.)").props("type=number step=0.001")
                recordenteredon = ui.input("Дата на въвеждане").props("type=date")

            def save_pok():
                data = {
                    "locationid": int(selected_layer.value) if selected_layer.value else None,
                    "type": type_field.value,
                    "quantity": int(quantity.value) if quantity.value else None,
                    "weight": float(weight.value) if weight.value else None,
                    "sok_weight": float(sok_weight.value) if sok_weight.value else None,
                    "recordenteredon": recordenteredon.value or str(date.today())
                }
                resp = create_pok(data)
                if resp and resp.status_code == 200:
                    ui.notify("✅ Записът е добавен успешно!")
                    refresh_table()
                    dialog.close()
                else:
                    ui.notify("❌ Грешка при добавяне!")

            with ui.row().classes("justify-end mt-4 gap-4"):
                ui.button("💾 Запиши", on_click=save_pok).classes("bg-green-500 text-white")
                ui.button("❌ Отказ", on_click=dialog.close)

        dialog.open()

    # === ✏️ Редактиране ===
    def open_edit_dialog(pok):
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-2xl p-6"):
            ui.label(f"✏️ Редакция на POK #{pok['pokid']}").classes("text-lg font-bold mb-2")

            with ui.grid(columns=2).classes("gap-4"):
                # selected_layer = ui.input("Локация ID", value=pok.get("locationid", ""))
                selected_layer = ui.select(options=layers_options, label="Локация")
                type_field = ui.input("Тип", value=pok.get("type", ""))
                quantity = ui.input("Количество", value=pok.get("quantity", "")).props("type=number")
                weight = ui.input("Тегло (гр.)", value=pok.get("weight", "")).props("type=number step=0.001")
                sok_weight = ui.input("Сок тегло (гр.)", value=pok.get("sok_weight", "")).props("type=number step=0.001")
                recordenteredon = ui.input("Дата", value=pok.get("recordenteredon", "")).props("type=date")

            def save_changes():
                data = {
                    "locationid": int(selected_layer.value) if selected_layer.value else None,
                    "type": type_field.value,
                    "quantity": int(quantity.value) if quantity.value else None,
                    "weight": float(weight.value) if weight.value else None,
                    "sok_weight": float(sok_weight.value) if sok_weight.value else None,
                    "recordenteredon": recordenteredon.value or str(date.today())
                }
                resp = update_pok(pok["pokid"], data)
                if resp and resp.status_code == 200:
                    ui.notify("✅ Промените са запазени!")
                    refresh_table()
                    dialog.close()
                else:
                    ui.notify("❌ Грешка при запис!")

            with ui.row().classes("justify-end mt-4 gap-4"):
                ui.button("💾 Запази", on_click=save_changes).classes("bg-green-500 text-white")
                ui.button("❌ Отказ", on_click=dialog.close)

        dialog.open()

    # === 🗑️ Изтриване ===
    def confirm_delete(pok):
        with ui.dialog() as confirm, ui.card().classes("w-full max-w-md p-4"):
            ui.label(f"❗ Изтриване на POK #{pok.get('pokid')}?").classes("text-lg")

            def do_delete():
                resp = delete_pok(pok["pokid"])
                if resp and getattr(resp, "status_code", None) == 200:
                    ui.notify("✅ Записът е изтрит!")
                    refresh_table()
                    confirm.close()
                else:
                    ui.notify("❌ Грешка при изтриване!")

            with ui.row().classes("justify-end gap-4 mt-4"):
                ui.button("Откажи", on_click=confirm.close)
                ui.button("🗑️ Изтрий", on_click=do_delete).classes("bg-red-500 text-white")

        confirm.open()

    # === Таблица ===
    def refresh_table():
        table_container.clear()
        pok_list = get_pok()
        if not pok_list:
            ui.label("⚠️ Няма въведени POK записи.").classes("text-gray-500 italic")
            return

        columns = [
            {"name": key, "label": field_labels[key], "field": key, "sortable": True}
            for key in field_labels.keys()
        ]
        columns.append({"name": "actions", "label": "Действия", "field": "actions"})

        rows = []
        for p in pok_list:
            row = {k: (p.get(k) if p.get(k) is not None else "-") for k in field_labels.keys()}
            row["actions"] = p
            rows.append(row)

        with table_container:
            table = ui.table(columns=columns, rows=rows, row_key="pokid", pagination=10)
            table.classes("w-full text-sm")
            table.add_slot("body-cell-actions", '''
                <q-td :props="props">
                    <q-btn size="sm" color="primary" flat icon="edit" @click="() => $parent.$emit('edit', props.row.actions)" />
                    <q-btn size="sm" color="negative" flat icon="delete" @click="() => $parent.$emit('delete', props.row.actions)" />
                </q-td>
            ''')
            table.on("edit", lambda e: open_edit_dialog(e.args))
            table.on("delete", lambda e: confirm_delete(e.args))

    # === Заглавие и бутон ===
    with ui.row().classes("justify-between w-full py-4"):
        ui.label("📐 Управление на POK").classes("text-xl font-bold")
        ui.button("➕ Нов запис", on_click=open_create_dialog).classes("bg-blue-500 text-white")

    # === Зареждане на таблицата ===
    refresh_table()
