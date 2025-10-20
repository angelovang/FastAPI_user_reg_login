from nicegui import ui
from datetime import date
from frontend.archaeology.api import (
    get_fragments,
    create_fragment,
    update_fragment,
    delete_fragment,
)

def show_fragments_dashboard():
    """Главен панел за управление на tblfragments (структура като при dashboard_pok)."""

    # --- Полета и преводи ---
    field_labels = {
        "fragmentid": "ID",
        "locationid": "Локация ID",
        "fragmenttype": "Тип фрагмент",
        "technology": "Технология",
        "baking": "Изпичане",
        "fract": "Фрактура",
        "primarycolor": "Основен цвят",
        "secondarycolor": "Вторичен цвят",
        "covering": "Покритие",
        "includesconc": "Конц. примеси",
        "includessize": "Размер примеси",
        "surface": "Повърхност",
        "count": "Брой",
        "onepot": "Един съд",
        "piecetype": "Тип част",
        "wallthickness": "Дебелина стена",
        "handletype": "Тип дръжка",
        "dishsize": "Размер съд",
        "bottomtype": "Тип дъно",
        "outline": "Контур",
        "category": "Категория",
        "form": "Форма",
        "type": "Тип",
        "subtype": "Подтип",
        "variant": "Вариант",
        "note": "Бележка",
        "inventory": "Инвентарен №",
        "recordenteredby": "Въведен от",
        "recordenteredon": "Въведен на"
    }

    # --- Енумерации ---
    enum_fragmenttype = ["1", "2"]
    enum_technology = ["1", "2", "2А", "2Б"]
    enum_dishsize = ["М", "С", "Г"]

    table_container = ui.column().classes("w-full")

    # Текущ потребител
    from frontend.common.session import get_session
    session = get_session()
    current_user = session.get("username", "")

    # === CRUD функции ===

    def open_create_dialog():
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-5xl p-6"):
            ui.label("➕ Нов фрагмент").classes("text-lg font-bold mb-2")

            with ui.grid(columns=4).classes("gap-3"):
                locationid = ui.input("Локация ID").props("type=number")
                fragmenttype = ui.select(enum_fragmenttype, label="Тип фрагмент")
                technology = ui.select(enum_technology, label="Технология")
                dishsize = ui.select(enum_dishsize, label="Размер съд")
                count = ui.input("Брой").props("type=number")
                note = ui.input("Бележка")
                recordenteredby = ui.input("Въведен от")
                recordenteredon = ui.input("Дата").props("type=date")

            def save_fragment():
                data = {
                    "locationid": int(locationid.value) if locationid.value else None,
                    "fragmenttype": fragmenttype.value,
                    "technology": technology.value,
                    "dishsize": dishsize.value,
                    "count": int(count.value) if count.value else 0,
                    "note": note.value,
                    "recordenteredby": recordenteredby.value,
                    "recordenteredon": recordenteredon.value or str(date.today())
                }
                resp = create_fragment(data)
                if resp and resp.status_code == 200:
                    ui.notify("✅ Фрагментът е добавен успешно!")
                    refresh_table()
                    dialog.close()
                else:
                    ui.notify("❌ Грешка при добавяне!")

            with ui.row().classes("justify-end mt-4 gap-4"):
                ui.button("💾 Запиши", on_click=save_fragment).classes("bg-green-500 text-white")
                ui.button("❌ Отказ", on_click=dialog.close)
        dialog.open()

    def open_edit_dialog(fragment):
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-5xl p-6"):
            ui.label(f"✏️ Редакция на фрагмент #{fragment['fragmentid']}").classes("text-lg font-bold mb-2")

            with ui.grid(columns=4).classes("gap-3"):
                locationid = ui.input("Локация ID", value=fragment.get("locationid"))
                fragmenttype = ui.select(enum_fragmenttype, value=fragment.get("fragmenttype"), label="Тип фрагмент")
                technology = ui.select(enum_technology, value=fragment.get("technology"), label="Технология")
                dishsize = ui.select(enum_dishsize, value=fragment.get("dishsize"), label="Размер съд")
                count = ui.input("Брой", value=fragment.get("count")).props("type=number")
                note = ui.input("Бележка", value=fragment.get("note"))
                recordenteredby = ui.input("Въведен от", value=fragment.get("recordenteredby"))
                recordenteredon = ui.input("Дата", value=fragment.get("recordenteredon")).props("type=date")

            def save_changes():
                data = {
                    "locationid": int(locationid.value) if locationid.value else None,
                    "fragmenttype": fragmenttype.value,
                    "technology": technology.value,
                    "dishsize": dishsize.value,
                    "count": int(count.value) if count.value else 0,
                    "note": note.value,
                    "recordenteredby": recordenteredby.value,
                    "recordenteredon": recordenteredon.value
                }
                resp = update_fragment(fragment["fragmentid"], data)
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

    def confirm_delete(fragment):
        with ui.dialog() as confirm, ui.card().classes("w-full max-w-md p-4"):
            ui.label(f"❗ Изтриване на фрагмент #{fragment.get('fragmentid')}?").classes("text-lg")

            def do_delete():
                resp = delete_fragment(fragment["fragmentid"])
                if resp and getattr(resp, "status_code", None) == 200:
                    ui.notify("✅ Фрагментът е изтрит!")
                    refresh_table()
                    confirm.close()
                else:
                    ui.notify("❌ Грешка при изтриване!")

            with ui.row().classes("justify-end gap-4 mt-4"):
                ui.button("Откажи", on_click=confirm.close)
                ui.button("🗑️ Изтрий", on_click=do_delete).classes("bg-red-500 text-white")
        confirm.open()

    # === Ляв панел с филтри + Дясна част с таблицата ===
    with ui.row().classes("w-full items-start no-wrap"):
        # --- Ляв панел ---
        with ui.column().classes(
            "w-[10%] min-w-[200px] gap-2 p-3 bg-gray-50 rounded-xl shadow-md sticky top-2 h-[90vh] overflow-auto"
        ):
            ui.label("🏺 Управление на фрагменти").classes("text-lg font-bold mb-2")

            ui.button("➕ Нов фрагмент", on_click=open_create_dialog).classes("bg-blue-500 text-white w-full")

            ui.separator().classes("my-2")
            ui.label("🔍 Филтри").classes("text-md font-semibold mb-2")

            # филтри
            filter_type = ui.input("Тип").props("clearable").classes("w-full")
            filter_tech = ui.input("Технология").props("clearable").classes("w-full")
            filter_dish = ui.input("Размер съд").props("clearable").classes("w-full")

            ui.separator().classes("my-2")

            ui.button("🎯 Приложи", on_click=lambda: refresh_table()).classes("bg-green-600 text-white w-full")

            def reset_filters():
                filter_type.value = ""
                filter_tech.value = ""
                filter_dish.value = ""
                refresh_table()

            ui.button("♻️ Нулирай", on_click=reset_filters).classes("bg-gray-400 text-white w-full")

        # --- Дясна зона: таблицата ---
        with ui.column().classes("w-[90%] p-1 overflow-auto"):
            table_container = ui.column().classes("w-full")

    # === Зареждане на таблицата ===
    def refresh_table():
        table_container.clear()
        fragments = get_fragments()
        if not fragments:
            ui.label("⚠️ Няма въведени фрагменти.").classes("text-gray-500 italic")
            return

        # филтриране
        filtered = []
        for frag in fragments:
            if filter_type.value and filter_type.value.lower() not in (str(frag.get("type", "")) or "").lower():
                continue
            if filter_tech.value and filter_tech.value.lower() not in (str(frag.get("technology", "")) or "").lower():
                continue
            if filter_dish.value and filter_dish.value.lower() not in (str(frag.get("dishsize", "")) or "").lower():
                continue
            filtered.append(frag)

        # колони
        all_fields = list(field_labels.keys())
        columns = [{"name": k, "label": field_labels[k], "field": k, "sortable": True} for k in all_fields]
        columns.append({"name": "actions", "label": "Управление на фрагменти", "field": "actions"})

        rows = []
        for frag in filtered:
            row = {k: (frag.get(k) if frag.get(k) is not None else "-") for k in all_fields}
            row["actions"] = frag
            rows.append(row)

        with table_container:
            table = ui.table(columns=columns, rows=rows, row_key="fragmentid", pagination=10)
            table.classes("w-full text-sm")
            table.add_slot("body-cell-actions", f'''
                 <q-td :props="props">
                     <template v-if="props.row.actions.recordenteredby === '{current_user}'">
                         <q-btn size="sm" color="primary" flat icon="edit"
                             @click="() => $parent.$emit('edit', props.row.actions)" />
                         <q-btn size="sm" color="negative" flat icon="delete"
                             @click="() => $parent.$emit('delete', props.row.actions)" />
                     </template>
                     <template v-else>
                         <q-icon name="lock" color="grey" size="sm" />
                     </template>
                 </q-td>
             ''')
            table.on("edit", lambda e: open_edit_dialog(e.args))
            table.on("delete", lambda e: confirm_delete(e.args))

    refresh_table()
