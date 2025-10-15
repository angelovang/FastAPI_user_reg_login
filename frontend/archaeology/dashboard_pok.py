from nicegui import ui
from datetime import date
from frontend.archaeology.api import (
    get_pok,
    create_pok,
    update_pok,
    delete_pok,
    get_layers,   # за dropdown избор на локация
)


def show_pok_dashboard():
    """Главен панел за управление на таблица tblpok (ляво: контроли, дясно: таблица)."""

    field_labels = {
        "pokid": "ID",
        "locationid": "Локация ID",
        "type": "Тип",
        "quantity": "Количество",
        "weight": "Тегло (гр.)",
        "sok_weight": "Сок тегло (гр.)",
        "recordenteredon": "Въведен на",
    }

    # контейнер за таблицата (ще се запълва в refresh_table)
    table_container = ui.column().classes("w-full")

    # зареждаме локациите за dropdown (използваме при диалозите)
    layers = get_layers() or []
    layers_options = {str(l["layerid"]): f"{l['layerid']} – {l.get('layername', '')}" for l in layers}

    # === функции за CRUD диалози (използвани под таблицата) ===
    def open_create_dialog():
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-2xl p-6"):
            ui.label("➕ Нов POK запис").classes("text-lg font-bold mb-2")

            with ui.grid(columns=2).classes("gap-4"):
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

    def open_edit_dialog(pok):
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-2xl p-6"):
            ui.label(f"✏️ Редакция на POK #{pok['pokid']}").classes("text-lg font-bold mb-2")

            with ui.grid(columns=2).classes("gap-4"):
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

    # === Лява колона (контроли) и дясна колона (таблица) ===
    # Следваме оформлението на dashboard_layers: ляв панел ~10% (sticky), дясна - 90%.
    with ui.row().classes("w-full items-start no-wrap"):

        # Ляв панел — ~10% (min width to keep usable)
        with ui.column().classes(
            "w-[10%] min-w-[180px] gap-2 p-2 bg-gray-50 rounded-xl shadow-md sticky top-2 h-[90vh] overflow-auto"
        ):
            ui.label("📐 Управление на POK").classes("text-lg font-bold mb-2")

            # Нов запис бутон
            ui.button("➕ Нов запис", on_click=open_create_dialog).classes("bg-blue-500 text-white w-full")

            ui.separator().classes("my-2")
            ui.label("🔍 Филтри").classes("text-md font-semibold mb-2")

            # Филтри (публични променливи, използвани в refresh_table)
            filter_type = ui.input("Тип").props("clearable").classes("w-full")
            filter_quantity = ui.input("Количество").props("type=number clearable").classes("w-full")

            ui.separator().classes("my-2")

            # Приложи / Нулирай бутони (под филтрите)
            ui.button("🎯 Приложи", on_click=lambda: refresh_table()).classes("bg-green-600 text-white w-full")

            def reset_filters():
                filter_type.value = ""
                filter_quantity.value = ""
                refresh_table()

            ui.button("♻️ Нулирай", on_click=reset_filters).classes("bg-gray-400 text-white w-full")

        # Дясна колона — таблица (90%)
        with ui.column().classes("w-[90%] p-1 overflow-auto"):
            table_container = ui.column().classes("w-full")

    # === Функция за попълване/refresh на таблицата ===
    def refresh_table():
        table_container.clear()
        pok_list = get_pok()
        if not pok_list:
            ui.label("⚠️ Няма въведени POK записи.").classes("text-gray-500 italic")
            return

        # Прилагаме филтрите от левия панел
        filtered = []
        for p in pok_list:
            # филтър по тип (частично търсене, case-insensitive)
            if filter_type.value and filter_type.value.lower() not in (str(p.get("type", "")) or "").lower():
                continue
            # филтър по количество (точно съвпадение, ако е зададено)
            if filter_quantity.value:
                try:
                    if int(p.get("quantity", 0)) != int(filter_quantity.value):
                        continue
                except Exception:
                    # ако input-a не може да се преобразува -> прескочи филтъра
                    pass
            filtered.append(p)

        # Подготовка на колони (последната колона е с етикет "Управление на POK")
        columns = [
            {"name": key, "label": field_labels[key], "field": key, "sortable": True}
            for key in field_labels.keys()
        ]
        columns.append({"name": "actions", "label": "Управление на POK", "field": "actions"})

        rows = []
        for p in filtered:
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

    # първоначално зареждане
    refresh_table()
