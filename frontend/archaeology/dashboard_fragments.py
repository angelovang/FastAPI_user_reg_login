from nicegui import ui
from datetime import date
from frontend.archaeology.api import (
    get_fragments,
    create_fragment,
    update_fragment,
    delete_fragment
)

def show_fragments_dashboard():
    """Главен панел за управление на tblfragments"""

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
        "includesconc": "Концентрация примеси",
        "includessize": "Размер примеси",
        "surface": "Повърхност",
        "count": "Брой",
        "onepot": "Един съд",
        "piecetype": "Тип част",
        "wallthickness": "Дебелина на стена",
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
    enum_baking = ["Р", "Н"]
    enum_fract = ["1", "2", "3"]
    enum_color = ["бял", "жълт", "охра", "червен", "сив", "тъмносив", "кафяв", "светлокафяв", "тъмнокафяв", "черен"]
    enum_covering = ["да", "не", "Ф1", "Ф2", "Б", "Г"]
    enum_includesconc = ["+", "-"]
    enum_includessize = ["М", "С", "Г"]
    enum_surface = ["А", "Б", "В", "В1", "В2", "Г"]
    enum_onepot = ["да", "не"]
    enum_piecetype = ["устие", "стена", "дръжка", "дъно", "профил", "чучур", "дъно+дръжка", "профил+дръжка",
                      "устие+дръжка", "стена+дръжка", "псевдочучур", "плавен прелом", "биконичност", "двоен съд", "цял съд"]
    enum_wallthickness = ["М", "С", "Г"]
    enum_dishsize = ["М", "С", "Г"]
    enum_bottomtype = ["А", "Б", "В", "А1", "А2", "Б1", "Б2", "В1", "В2"]
    enum_outline = ["1", "2", "3"]

    table_container = ui.column().classes("w-full")

    # === 🟢 Създаване ===
    def open_create_dialog():
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-5xl p-6"):
            ui.label("➕ Нов фрагмент").classes("text-lg font-bold mb-2")

            with ui.grid(columns=4).classes("gap-3"):
                locationid = ui.input("Локация ID").props("type=number")
                fragmenttype = ui.select(enum_fragmenttype, label="Тип фрагмент")
                technology = ui.select(enum_technology, label="Технология")
                baking = ui.select(enum_baking, label="Изпичане")
                fract = ui.select(enum_fract, label="Фрактура")
                primarycolor = ui.select(enum_color, label="Основен цвят")
                secondarycolor = ui.select(enum_color, label="Вторичен цвят")
                covering = ui.select(enum_covering, label="Покритие")
                includesconc = ui.select(enum_includesconc, label="Конц. примеси")
                includessize = ui.select(enum_includessize, label="Размер примеси")
                surface = ui.select(enum_surface, label="Повърхност")
                count = ui.input("Брой").props("type=number")
                onepot = ui.select(enum_onepot, label="Един съд")
                piecetype = ui.select(enum_piecetype, label="Тип част")
                wallthickness = ui.select(enum_wallthickness, label="Дебелина стена")
                handletype = ui.input("Тип дръжка")
                dishsize = ui.select(enum_dishsize, label="Размер съд")
                bottomtype = ui.select(enum_bottomtype, label="Тип дъно")
                outline = ui.select(enum_outline, label="Контур")
                category = ui.input("Категория")
                form = ui.input("Форма")
                type_ = ui.input("Тип")
                subtype = ui.input("Подтип")
                variant = ui.input("Вариант")
                note = ui.input("Бележка")
                inventory = ui.input("Инвентарен №")
                recordenteredby = ui.input("Въведен от")
                recordenteredon = ui.input("Дата").props("type=date")

            def save_fragment():
                data = {
                    "locationid": int(locationid.value) if locationid.value else None,
                    "fragmenttype": fragmenttype.value,
                    "technology": technology.value,
                    "baking": baking.value,
                    "fract": fract.value,
                    "primarycolor": primarycolor.value,
                    "secondarycolor": secondarycolor.value,
                    "covering": covering.value,
                    "includesconc": includesconc.value,
                    "includessize": includessize.value,
                    "surface": surface.value,
                    "count": int(count.value) if count.value else 0,
                    "onepot": onepot.value,
                    "piecetype": piecetype.value,
                    "wallthickness": wallthickness.value,
                    "handletype": handletype.value,
                    "dishsize": dishsize.value,
                    "bottomtype": bottomtype.value,
                    "outline": outline.value,
                    "category": category.value,
                    "form": form.value,
                    "type": int(type_.value) if type_.value else None,
                    "subtype": subtype.value,
                    "variant": int(variant.value) if variant.value else None,
                    "note": note.value,
                    "inventory": inventory.value,
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

    # === ✏️ Редакция ===
    def open_edit_dialog(fragment):
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-5xl p-6"):
            ui.label(f"✏️ Редакция на фрагмент #{fragment['fragmentid']}").classes("text-lg font-bold mb-2")

            with ui.grid(columns=4).classes("gap-3"):
                locationid = ui.input("Локация ID", value=fragment.get("locationid"))
                fragmenttype = ui.select(enum_fragmenttype, value=fragment.get("fragmenttype"), label="Тип фрагмент")
                technology = ui.select(enum_technology, value=fragment.get("technology"), label="Технология")
                baking = ui.select(enum_baking, value=fragment.get("baking"), label="Изпичане")
                fract = ui.select(enum_fract, value=fragment.get("fract"), label="Фрактура")
                primarycolor = ui.select(enum_color, value=fragment.get("primarycolor"), label="Основен цвят")
                secondarycolor = ui.select(enum_color, value=fragment.get("secondarycolor"), label="Вторичен цвят")
                covering = ui.select(enum_covering, value=fragment.get("covering"), label="Покритие")
                includesconc = ui.select(enum_includesconc, value=fragment.get("includesconc"), label="Конц. примеси")
                includessize = ui.select(enum_includessize, value=fragment.get("includessize"), label="Размер примеси")
                surface = ui.select(enum_surface, value=fragment.get("surface"), label="Повърхност")
                count = ui.input("Брой", value=fragment.get("count")).props("type=number")
                onepot = ui.select(enum_onepot, value=fragment.get("onepot"), label="Един съд")
                piecetype = ui.select(enum_piecetype, value=fragment.get("piecetype"), label="Тип част")
                wallthickness = ui.select(enum_wallthickness, value=fragment.get("wallthickness"), label="Дебелина стена")
                handletype = ui.input("Тип дръжка", value=fragment.get("handletype"))
                dishsize = ui.select(enum_dishsize, value=fragment.get("dishsize"), label="Размер съд")
                bottomtype = ui.select(enum_bottomtype, value=fragment.get("bottomtype"), label="Тип дъно")
                outline = ui.select(enum_outline, value=fragment.get("outline"), label="Контур")
                category = ui.input("Категория", value=fragment.get("category"))
                form = ui.input("Форма", value=fragment.get("form"))
                type_ = ui.input("Тип", value=fragment.get("type"))
                subtype = ui.input("Подтип", value=fragment.get("subtype"))
                variant = ui.input("Вариант", value=fragment.get("variant"))
                note = ui.input("Бележка", value=fragment.get("note"))
                inventory = ui.input("Инвентарен №", value=fragment.get("inventory"))
                recordenteredby = ui.input("Въведен от", value=fragment.get("recordenteredby"))
                recordenteredon = ui.input("Дата", value=fragment.get("recordenteredon")).props("type=date")

            def save_changes():
                data = {
                    "locationid": int(locationid.value) if locationid.value else None,
                    "fragmenttype": fragmenttype.value,
                    "technology": technology.value,
                    "baking": baking.value,
                    "fract": fract.value,
                    "primarycolor": primarycolor.value,
                    "secondarycolor": secondarycolor.value,
                    "covering": covering.value,
                    "includesconc": includesconc.value,
                    "includessize": includessize.value,
                    "surface": surface.value,
                    "count": int(count.value) if count.value else 0,
                    "onepot": onepot.value,
                    "piecetype": piecetype.value,
                    "wallthickness": wallthickness.value,
                    "handletype": handletype.value,
                    "dishsize": dishsize.value,
                    "bottomtype": bottomtype.value,
                    "outline": outline.value,
                    "category": category.value,
                    "form": form.value,
                    "type": int(type_.value) if type_.value else None,
                    "subtype": subtype.value,
                    "variant": int(variant.value) if variant.value else None,
                    "note": note.value,
                    "inventory": inventory.value,
                    "recordenteredby": recordenteredby.value,
                    "recordenteredon": recordenteredon.value,
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

    # === 🗑️ Изтриване ===
    def confirm_delete(fragment):
        with ui.dialog() as confirm, ui.card().classes("w-full max-w-xl p-4"):
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

    # === Таблица ===
    def refresh_table():
        table_container.clear()
        fragments = get_fragments()
        if not fragments:
            ui.label("⚠️ Няма въведени фрагменти.").classes("text-gray-500 italic")
            return

        all_fields = list(field_labels.keys())
        columns = [{"name": k, "label": field_labels[k], "field": k, "sortable": True} for k in all_fields]
        columns.append({"name": "actions", "label": "Действия", "field": "actions"})

        rows = []
        for frag in fragments:
            row = {k: (frag.get(k) if frag.get(k) is not None else "-") for k in all_fields}
            row["actions"] = frag
            rows.append(row)

        with table_container:
            table = ui.table(columns=columns, rows=rows, row_key="fragmentid", pagination=10)
            table.classes("w-full text-sm")
            table.add_slot("body-cell-actions", '''
                <q-td :props="props">
                    <q-btn size="sm" color="primary" flat icon="edit" @click="() => $parent.$emit('edit', props.row.actions)" />
                    <q-btn size="sm" color="negative" flat icon="delete" @click="() => $parent.$emit('delete', props.row.actions)" />
                </q-td>
            ''')
            table.on("edit", lambda e: open_edit_dialog(e.args))
            table.on("delete", lambda e: confirm_delete(e.args))

    # === Заглавие ===
    with ui.row().classes("justify-between w-full py-4"):
        ui.label("🏺 Управление на фрагменти").classes("text-xl font-bold")
        ui.button("➕ Нов фрагмент", on_click=open_create_dialog).classes("bg-blue-500 text-white")

    refresh_table()
