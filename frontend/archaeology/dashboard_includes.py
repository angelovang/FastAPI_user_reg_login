from nicegui import ui
from datetime import date
from frontend.archaeology.api import (
    get_layer_includes,
    create_layer_include,
    update_layer_include,
    delete_layer_include
)


def show_layer_includes_dashboard():
    """Главен панел за управление на tbllayerincludes"""

    # === Конфигурация на полета ===
    field_labels = {
        "includeid": "ID",
        "locationid": "Локация ID",
        "includetype": "Тип примес",
        "includetext": "Описание",
        "includesize": "Размер",
        "includeconc": "Концентрация",
        "recordenteredon": "Въведен на",
    }

    enum_includetype = ["антропогенен", "естествен"]
    enum_includesize = ["малки", "средни", "големи"]
    enum_includeconc = ["ниска", "средна", "висока"]

    table_container = ui.column().classes("w-full")

    # === 🟢 Форма за създаване ===
    def open_create_dialog():
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-3xl p-6"):
            ui.label("➕ Нов примес").classes("text-lg font-bold mb-2")

            with ui.grid(columns=2).classes("gap-4"):
                locationid = ui.input("Локация ID").props("type=number")
                includetype = ui.select(enum_includetype, label="Тип примес")
                includetext = ui.input("Описание на примеса")
                includesize = ui.select(enum_includesize, label="Размер")
                includeconc = ui.select(enum_includeconc, label="Концентрация")
                recordenteredon = ui.input("Въведен на").props("type=date")

            def save_include():
                data = {
                    "locationid": int(locationid.value) if locationid.value else None,
                    "includetype": includetype.value,
                    "includetext": includetext.value,
                    "includesize": includesize.value,
                    "includeconc": includeconc.value,
                    "recordenteredon": recordenteredon.value or str(date.today()),
                }
                resp = create_layer_include(data)
                if resp and resp.status_code == 200:
                    ui.notify("✅ Примесът е добавен успешно!")
                    refresh_table()
                    dialog.close()
                else:
                    ui.notify("❌ Грешка при добавяне!")

            with ui.row().classes("justify-end mt-4 gap-4"):
                ui.button("💾 Запиши", on_click=save_include).classes("bg-green-500 text-white")
                ui.button("❌ Отказ", on_click=dialog.close)

        dialog.open()

    # === ✏️ Редакция ===
    def open_edit_dialog(include):
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-3xl p-6"):
            ui.label(f"✏️ Редакция на примес #{include['includeid']}").classes("text-lg font-bold mb-2")

            with ui.grid(columns=2).classes("gap-4"):
                locationid = ui.input("Локация ID", value=include.get("locationid", ""))
                includetype = ui.select(enum_includetype, value=include.get("includetype"), label="Тип примес")
                includetext = ui.input("Описание", value=include.get("includetext", ""))
                includesize = ui.select(enum_includesize, value=include.get("includesize"), label="Размер")
                includeconc = ui.select(enum_includeconc, value=include.get("includeconc"), label="Концентрация")
                recordenteredon = ui.input("Въведен на", value=include.get("recordenteredon", "")).props("type=date")

            def save_changes():
                data = {
                    "locationid": int(locationid.value) if locationid.value else None,
                    "includetype": includetype.value,
                    "includetext": includetext.value,
                    "includesize": includesize.value,
                    "includeconc": includeconc.value,
                    "recordenteredon": recordenteredon.value,
                }
                resp = update_layer_include(include["includeid"], data)
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
    def confirm_delete(include):
        with ui.dialog() as confirm, ui.card().classes("w-full max-w-xl p-4"):
            ui.label(f"❗ Изтриване на примес '{include.get('includetext', '(без име)')}'?").classes("text-lg")

            def do_delete():
                resp = delete_layer_include(include["includeid"])
                if resp and getattr(resp, "status_code", None) == 200:
                    ui.notify("✅ Примесът е изтрит!")
                    refresh_table()
                    confirm.close()
                else:
                    ui.notify("❌ Грешка при изтриване!")

            with ui.row().classes("justify-end gap-4 mt-4"):
                ui.button("Откажи", on_click=confirm.close)
                ui.button("🗑️ Изтрий", on_click=do_delete).classes("bg-red-500 text-white")

        confirm.open()

    # === 🔄 Таблица ===
    def refresh_table():
        table_container.clear()
        includes = get_layer_includes()
        if not includes:
            ui.label("⚠️ Няма въведени примеси.").classes("text-gray-500 italic")
            return

        filtered_includes = []
        for inc in includes:
            if filter_text.value and filter_text.value.lower() not in (inc.get("includetext") or "").lower():
                continue
            if filter_type.value and inc.get("includetype") != filter_type.value:
                continue
            if filter_conc.value and inc.get("includeconc") != filter_conc.value:
                continue
            filtered_includes.append(inc)

        all_fields = list(field_labels.keys())
        columns = [{"name": k, "label": field_labels[k], "field": k, "sortable": True} for k in all_fields]
        columns.append({"name": "actions", "label": "Действия", "field": "actions"})

        rows = []
        for inc in filtered_includes:
            row = {k: (inc.get(k) if inc.get(k) is not None else "-") for k in all_fields}
            row["actions"] = inc
            rows.append(row)

        with table_container:
            table = ui.table(columns=columns, rows=rows, row_key="includeid", pagination=10)
            table.classes("w-full text-sm")
            table.add_slot("body-cell-actions", '''
                <q-td :props="props">
                    <q-btn size="sm" color="primary" flat icon="edit"
                           @click="() => $parent.$emit('edit', props.row.actions)" />
                    <q-btn size="sm" color="negative" flat icon="delete"
                           @click="() => $parent.$emit('delete', props.row.actions)" />
                </q-td>
            ''')
            table.on("edit", lambda e: open_edit_dialog(e.args))
            ui.on("delete", lambda e: confirm_delete(e.args))

    # === Ляв панел + Таблица ===
    with ui.row().classes("w-full items-start no-wrap"):
        # 🎛️ Ляв панел (бутони и филтри)
        with ui.column().classes(
            "w-[5%] min-w-[180px] gap-2 p-2 bg-gray-50 rounded-xl shadow-md sticky top-2 h-[90vh] overflow-auto"
        ):
            ui.label("⚗️ Управление на примеси").classes("text-lg font-bold mb-2")

            ui.button("➕ Нов примес", on_click=open_create_dialog).classes("bg-blue-500 text-white w-full")

            ui.separator().classes("my-2")

            ui.label("🔍 Филтриране по:").classes("text-md font-semibold mb-2")

            filter_text = ui.input("Описание").props("clearable").classes("w-full")
            filter_type = ui.select([""] + enum_includetype, label="Тип примес").classes("w-full")
            filter_conc = ui.select([""] + enum_includeconc, label="Концентрация").classes("w-full")

            ui.separator().classes("my-2")

            ui.button("🎯 Приложи", on_click=lambda: refresh_table()).classes("bg-green-600 text-white w-full")

            def reset_filters():
                filter_text.value = ""
                filter_type.value = ""
                filter_conc.value = ""
                refresh_table()

            ui.button("♻️ Нулирай", on_click=reset_filters).classes("bg-gray-400 text-white w-full")

        # 📋 Таблица вдясно
        with ui.column().classes("w-[90%] p-1 overflow-auto"):
            table_container = ui.column().classes("w-full")

    # === Първоначално зареждане ===
    refresh_table()
