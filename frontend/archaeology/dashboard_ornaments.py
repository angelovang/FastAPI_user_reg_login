from nicegui import ui
from datetime import date
from frontend.archaeology.api import (
    get_ornaments,
    create_ornament,
    update_ornament,
    delete_ornament,
    get_fragments,
)


def show_ornaments_dashboard():
    """Главен панел за управление на tblornaments (със същата структура като при fragments/pok)."""

    # --- Полета и преводи ---
    field_labels = {
        "ornamentid": "ID",
        "fragmentid": "Фрагмент ID",
        "location": "Локация",
        "relationship": "Връзка",
        "onornament": "Върху орнамент",
        "encrustcolor1": "Основен цвят",
        "encrustcolor2": "Вторичен цвят",
        "primary_": "Основна форма",
        "secondary": "Вторична форма",
        "tertiary": "Третична форма",
        "quarternary": "Кварт.",
        "recordenteredon": "Въведен на",
    }

    enum_primary = ['А', 'В', 'Д', 'И', 'К', 'Н', 'П', 'Р', 'Ф', 'Ц', 'Щ']
    enum_secondary = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
                      'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']
    enum_tertiary = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М',
                     'П', 'А1', 'А2', 'Б1', 'Б2']

    table_container = ui.column().classes("w-full")

    # === CRUD функции ===
    def open_create_dialog():
        fragments = get_fragments()
        fragment_options = [f"{f['fragmentid']} – {f.get('piecetype', '')}" for f in fragments]

        with ui.dialog() as dialog, ui.card().classes("w-full max-w-4xl p-6"):
            ui.label("➕ Нов орнамент").classes("text-lg font-bold mb-4")

            with ui.grid(columns=2).classes("gap-4"):
                fragment_select = ui.select(fragment_options, label="Фрагмент")
                location = ui.input("Локация")
                relationship = ui.input("Връзка")
                onornament = ui.input("Върху орнамент").props("type=number")
                encrustcolor1 = ui.input("Основен цвят")
                encrustcolor2 = ui.input("Вторичен цвят")
                primary_ = ui.select(enum_primary, label="Основна форма")
                secondary = ui.select(enum_secondary, label="Вторична форма")
                tertiary = ui.select(enum_tertiary, label="Третична форма")
                quarternary = ui.input("Кварт.").props("type=number")
                recordenteredon = ui.input("Въведен на").props("type=date")

            def save_ornament():
                frag_id = None
                if fragment_select.value:
                    frag_id = int(fragment_select.value.split("–")[0].strip())

                data = {
                    "fragmentid": frag_id,
                    "location": location.value,
                    "relationship": relationship.value,
                    "onornament": int(onornament.value) if onornament.value else None,
                    "encrustcolor1": encrustcolor1.value,
                    "encrustcolor2": encrustcolor2.value,
                    "primary_": primary_.value,
                    "secondary": secondary.value,
                    "tertiary": tertiary.value,
                    "quarternary": int(quarternary.value) if quarternary.value else None,
                    "recordenteredon": recordenteredon.value or str(date.today()),
                }

                resp = create_ornament(data)
                if resp and resp.status_code == 200:
                    ui.notify("✅ Орнаментът е добавен успешно!")
                    refresh_table()
                    dialog.close()
                else:
                    ui.notify("❌ Грешка при добавяне!")

            with ui.row().classes("justify-end mt-4 gap-4"):
                ui.button("💾 Запиши", on_click=save_ornament).classes("bg-green-500 text-white")
                ui.button("❌ Отказ", on_click=dialog.close)

        dialog.open()

    def open_edit_dialog(ornament):
        fragments = get_fragments()
        fragment_options = [f"{f['fragmentid']} – {f.get('piecetype', '')}" for f in fragments]
        current_fragment = next(
            (f for f in fragment_options if f.startswith(str(ornament.get("fragmentid", "")))), None
        )

        with ui.dialog() as dialog, ui.card().classes("w-full max-w-4xl p-6"):
            ui.label(f"✏️ Редакция на орнамент #{ornament['ornamentid']}").classes("text-lg font-bold mb-4")

            with ui.grid(columns=2).classes("gap-4"):
                fragment_select = ui.select(fragment_options, value=current_fragment, label="Фрагмент")
                location = ui.input("Локация", value=ornament.get("location", ""))
                relationship = ui.input("Връзка", value=ornament.get("relationship", ""))
                onornament = ui.input("Върху орнамент", value=ornament.get("onornament", "")).props("type=number")
                encrustcolor1 = ui.input("Основен цвят", value=ornament.get("encrustcolor1", ""))
                encrustcolor2 = ui.input("Вторичен цвят", value=ornament.get("encrustcolor2", ""))
                primary_ = ui.select(enum_primary, value=ornament.get("primary_"), label="Основна форма")
                secondary = ui.select(enum_secondary, value=ornament.get("secondary"), label="Вторична форма")
                tertiary = ui.select(enum_tertiary, value=ornament.get("tertiary"), label="Третична форма")
                quarternary = ui.input("Кварт.", value=ornament.get("quarternary", "")).props("type=number")
                recordenteredon = ui.input("Въведен на", value=ornament.get("recordenteredon", "")).props("type=date")

            def save_changes():
                frag_id = None
                if fragment_select.value:
                    frag_id = int(fragment_select.value.split("–")[0].strip())

                data = {
                    "fragmentid": frag_id,
                    "location": location.value,
                    "relationship": relationship.value,
                    "onornament": int(onornament.value) if onornament.value else None,
                    "encrustcolor1": encrustcolor1.value,
                    "encrustcolor2": encrustcolor2.value,
                    "primary_": primary_.value,
                    "secondary": secondary.value,
                    "tertiary": tertiary.value,
                    "quarternary": int(quarternary.value) if quarternary.value else None,
                    "recordenteredon": recordenteredon.value,
                }

                resp = update_ornament(ornament["ornamentid"], data)
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

    def confirm_delete(ornament):
        with ui.dialog() as confirm, ui.card().classes("w-full max-w-xl p-4"):
            ui.label(f"❗ Изтриване на орнамент ID {ornament['ornamentid']}?").classes("text-lg")

            def do_delete():
                resp = delete_ornament(ornament["ornamentid"])
                if resp and getattr(resp, "status_code", None) == 200:
                    ui.notify("✅ Орнаментът е изтрит!")
                    refresh_table()
                    confirm.close()
                else:
                    ui.notify("❌ Грешка при изтриване!")

            with ui.row().classes("justify-end gap-4 mt-4"):
                ui.button("Откажи", on_click=confirm.close)
                ui.button("🗑️ Изтрий", on_click=do_delete).classes("bg-red-500 text-white")

        confirm.open()

    # === Layout ===
    with ui.row().classes("w-full items-start no-wrap"):
        # --- Ляв панел ---
        with ui.column().classes(
            "w-[10%] min-w-[220px] gap-2 p-3 bg-gray-50 rounded-xl shadow-md sticky top-2 h-[90vh] overflow-auto"
        ):
            ui.label("🎨 Управление на орнаменти").classes("text-lg font-bold mb-2")

            ui.button("➕ Нов орнамент", on_click=open_create_dialog).classes("bg-blue-500 text-white w-full")

            ui.separator().classes("my-2")
            ui.label("🔍 Филтри").classes("text-md font-semibold mb-2")

            filter_location = ui.input("Локация").props("clearable").classes("w-full")
            filter_color = ui.input("Основен цвят").props("clearable").classes("w-full")
            filter_primary = ui.input("Основна форма").props("clearable").classes("w-full")

            ui.separator().classes("my-2")

            ui.button("🎯 Приложи", on_click=lambda: refresh_table()).classes("bg-green-600 text-white w-full")

            def reset_filters():
                filter_location.value = ""
                filter_color.value = ""
                filter_primary.value = ""
                refresh_table()

            ui.button("♻️ Нулирай", on_click=reset_filters).classes("bg-gray-400 text-white w-full")

        # --- Дясна зона ---
        with ui.column().classes("w-[90%] p-1 overflow-auto"):
            table_container = ui.column().classes("w-full")

    # === Таблица с филтриране ===
    def refresh_table():
        table_container.clear()
        ornaments = get_ornaments()
        if not ornaments:
            ui.label("⚠️ Няма въведени орнаменти.").classes("text-gray-500 italic")
            return

        filtered = []
        for orn in ornaments:
            if filter_location.value and filter_location.value.lower() not in (orn.get("location", "") or "").lower():
                continue
            if filter_color.value and filter_color.value.lower() not in (orn.get("encrustcolor1", "") or "").lower():
                continue
            if filter_primary.value and filter_primary.value.lower() not in (orn.get("primary_", "") or "").lower():
                continue
            filtered.append(orn)

        columns = [{"name": k, "label": field_labels[k], "field": k, "sortable": True} for k in field_labels]
        columns.append({"name": "actions", "label": "Управление на орнаменти", "field": "actions"})

        rows = []
        for orn in filtered:
            row = {k: orn.get(k, "-") for k in field_labels}
            row["actions"] = orn
            rows.append(row)

        with table_container:
            table = ui.table(columns=columns, rows=rows, row_key="ornamentid", pagination=10)
            table.classes("w-full text-sm")
            table.add_slot("body-cell-actions", '''
                <q-td :props="props">
                    <q-btn size="sm" color="primary" flat icon="edit" @click="() => $parent.$emit('edit', props.row.actions)" />
                    <q-btn size="sm" color="negative" flat icon="delete" @click="() => $parent.$emit('delete', props.row.actions)" />
                </q-td>
            ''')
            table.on("edit", lambda e: open_edit_dialog(e.args))
            table.on("delete", lambda e: confirm_delete(e.args))

    refresh_table()
