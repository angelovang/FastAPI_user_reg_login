from nicegui import ui
from frontend.archaeology.api import get_layers, create_layer, update_layer, delete_layer


def show_layers_dashboard():
    """Главен панел за управление на tbllayers"""

    # === Конфигурация на полета ===
    enum_layertype = ['механичен', 'контекст']
    enum_colors = [
        'бял', 'жълт', 'охра', 'червен', 'сив',
        'тъмносив', 'кафяв', 'светлокафяв', 'тъмнокафяв', 'черен'
    ]

    field_labels = {
        "layerid": "ID",
        "layername": "Име на пласт",
        "layertype": "Тип пласт",
        "site": "Обект",
        "sector": "Сектор",
        "square": "Квадрат",
        "context": "Контекст",
        "layer": "Пласт",
        "stratum": "Стратиграфия",
        "parentid": "Родител ID",
        "level": "Ниво",
        "structure": "Структура",
        "includes": "Примеси",
        "color1": "Основен цвят",
        "color2": "Вторичен цвят",
        "handfragments": "Ръчни фрагменти",
        "wheelfragment": "Колесни фрагменти",
        "recordenteredby": "Въведен от",
        "recordenteredon": "Въведен на",
        "recordcreatedby": "Създаден от",
        "recordcreatedon": "Създаден на",
        "description": "Описание",
        "akb_num": "АКБ №",
    }

    table_container = ui.column().classes("w-full")

    # Текущ потребител
    from frontend.common.session import get_session
    session = get_session()
    current_user = session.get("username", "")

    # === 🟢 Форма за създаване ===
    def open_create_dialog():
        from frontend.common.session import get_session
        session = get_session()
        username = session.get("username", "")  # fallback ако не е логнат

        with ui.dialog() as dialog, ui.card().classes("w-full max-w-5xl p-6"):
            ui.label("➕ Нов пласт").classes("text-lg font-bold mb-2")

            with ui.grid(columns=4).classes("gap-4"):
                layername = ui.input("Име на пласт")
                layertype = ui.select(["механичен", "контекст"], label="Тип пласт")
                site = ui.input("Обект")
                sector = ui.input("Сектор")
                square = ui.input("Квадрат")
                context = ui.input("Контекст")
                layer = ui.input("Слой")
                stratum = ui.input("Стратиграфия")
                parentid = ui.input("Parent ID").props("type=number")
                level = ui.input("Ниво")
                structure = ui.input("Структура")
                includes = ui.input("Съдържа")
                color1 = ui.select(
                    ['бял', 'жълт', 'охра', 'червен', 'сив', 'тъмносив', 'кафяв', 'светлокафяв', 'тъмнокафяв', 'черен'],
                    label="Основен цвят"
                )
                color2 = ui.select(
                    ['бял', 'жълт', 'охра', 'червен', 'сив', 'тъмносив', 'кафяв', 'светлокафяв', 'тъмнокафяв', 'черен'],
                    label="Втори цвят"
                )
                handfragments = ui.input("Ръчни фрагменти").props("type=number")
                wheelfragment = ui.input("Грънчарски фрагменти").props("type=number")
                recordenteredby = ui.input("Въведен от", value=username)
                recordenteredon = ui.input("Въведен на").props("type=date")
                recordcreatedby = ui.input("Създаден от", value=username)
                recordcreatedon = ui.input("Създаден на").props("type=date")
                description = ui.textarea("Описание")
                akb_num = ui.input("AKB №").props("type=number")

            def save_layer():
                data = {
                    "layername": layername.value,
                    "layertype": layertype.value,
                    "site": site.value,
                    "sector": sector.value,
                    "square": square.value,
                    "context": context.value,
                    "layer": layer.value,
                    "stratum": stratum.value,
                    "parentid": int(parentid.value) if parentid.value else None,
                    "level": level.value,
                    "structure": structure.value,
                    "includes": includes.value,
                    "color1": color1.value,
                    "color2": color2.value,
                    "handfragments": int(handfragments.value) if handfragments.value else None,
                    "wheelfragment": int(wheelfragment.value) if wheelfragment.value else None,
                    "recordenteredby": recordenteredby.value,
                    "recordenteredon": recordenteredon.value,
                    "recordcreatedby": recordcreatedby.value,
                    "recordcreatedon": recordcreatedon.value,
                    "description": description.value,
                    "akb_num": int(akb_num.value) if akb_num.value else None,
                }
                resp = create_layer(data)
                if resp and resp.status_code == 200:
                    ui.notify("✅ Пластът е добавен!")
                    refresh_table()
                    dialog.close()
                else:
                    ui.notify("❌ Грешка при добавяне!")

            with ui.row().classes("justify-end mt-4 gap-4"):
                ui.button("💾 Запиши", on_click=save_layer).classes("bg-green-500 text-white")
                ui.button("❌ Отказ", on_click=dialog.close)

        dialog.open()

    # === 🔁 Обновяване на таблицата ===
    def refresh_table():
        table_container.clear()
        layers = get_layers()
        if not layers:
            ui.label("⚠️ Няма налични записи.").classes("text-gray-500 italic")
            return

        # === Филтриране ===
        filtered_layers = []
        for l in layers:
            if filter_name.value and filter_name.value.lower() not in (l.get('layername') or '').lower():
                continue
            if filter_type.value and l.get('layertype') != filter_type.value:
                continue
            if filter_color.value and l.get('color1') != filter_color.value:
                continue
            filtered_layers.append(l)

        all_fields = list(field_labels.keys())
        columns = [{"name": key, "label": field_labels[key], "field": key, "sortable": True} for key in all_fields]
        columns.append({"name": "actions", "label": "Действия", "field": "actions"})

        rows = []
        for l in filtered_layers:
            row = {key: (l.get(key) if l.get(key) is not None else "-") for key in all_fields}
            row["actions"] = l
            rows.append(row)

        with table_container:
            table = ui.table(columns=columns, rows=rows, row_key="layerid", pagination=10)
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

        all_fields = list(field_labels.keys())
        columns = [{"name": key, "label": field_labels[key], "field": key, "sortable": True} for key in all_fields]
        columns.append({"name": "actions", "label": "Действия", "field": "actions"})

    # === ✏️ Форма за редакция ===
    def open_edit_dialog(layer):
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-5xl p-6"):
            ui.label(f"✏️ Редакция на пласт #{layer['layerid']}").classes("text-lg font-bold mb-2")

            with ui.grid(columns=4).classes("gap-4"):
                layername = ui.input("Име на пласт", value=layer.get("layername", ""))
                layertype = ui.select(["механичен", "контекст"], value=layer.get("layertype"), label="Тип пласт")
                site = ui.input("Обект", value=layer.get("site", ""))
                sector = ui.input("Сектор", value=layer.get("sector", ""))
                square = ui.input("Квадрат", value=layer.get("square", ""))
                context = ui.input("Контекст", value=layer.get("context", ""))
                layer_field = ui.input("Слой", value=layer.get("layer", ""))
                stratum = ui.input("Стратиграфия", value=layer.get("stratum", ""))
                parentid = ui.input("Parent ID", value=layer.get("parentid", ""))
                level = ui.input("Ниво", value=layer.get("level", ""))
                structure = ui.input("Структура", value=layer.get("structure", ""))
                includes = ui.input("Съдържа", value=layer.get("includes", ""))
                color1 = ui.select(
                    ['бял', 'жълт', 'охра', 'червен', 'сив', 'тъмносив', 'кафяв', 'светлокафяв', 'тъмнокафяв', 'черен'],
                    value=layer.get("color1"), label="Основен цвят"
                )
                color2 = ui.select(
                    ['бял', 'жълт', 'охра', 'червен', 'сив', 'тъмносив', 'кафяв', 'светлокафяв', 'тъмнокафяв', 'черен'],
                    value=layer.get("color2"), label="Втори цвят"
                )
                handfragments = ui.input("Ръчни фрагменти", value=layer.get("handfragments", ""))
                wheelfragment = ui.input("Грънчарско колело", value=layer.get("wheelfragment", ""))
                recordenteredby = ui.input("Въведен от", value=layer.get("recordenteredby", ""))
                recordenteredon = ui.input("Въведен на", value=layer.get("recordenteredon", ""))
                recordcreatedby = ui.input("Създаден от", value=layer.get("recordcreatedby", ""))
                recordcreatedon = ui.input("Създаден на", value=layer.get("recordcreatedon", ""))
                description = ui.textarea("Описание", value=layer.get("description", ""))
                akb_num = ui.input("АКБ №", value=layer.get("akb_num", ""))

            def save_changes():
                data = {
                    "layername": layername.value,
                    "layertype": layertype.value,
                    "site": site.value,
                    "sector": sector.value,
                    "square": square.value,
                    "context": context.value,
                    "layer": layer_field.value,
                    "stratum": stratum.value,
                    "parentid": int(parentid.value) if parentid.value else None,
                    "level": level.value,
                    "structure": structure.value,
                    "includes": includes.value,
                    "color1": color1.value,
                    "color2": color2.value,
                    "handfragments": int(handfragments.value) if handfragments.value else None,
                    "wheelfragment": int(wheelfragment.value) if wheelfragment.value else None,
                    "recordenteredby": recordenteredby.value,
                    "recordenteredon": recordenteredon.value,
                    "recordcreatedby": recordcreatedby.value,
                    "recordcreatedon": recordcreatedon.value,
                    "description": description.value,
                    "akb_num": int(akb_num.value) if akb_num.value else None,
                }
                resp = update_layer(layer["layerid"], data)
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

    # === 🗑️ Потвърждение за изтриване ===
    def confirm_delete(layer):
        with ui.dialog() as confirm, ui.card().classes("w-full max-w-xl p-4"):
            ui.label(f"❗ Изтриване на слой'{layer.get('layername', '(без име)')}'?").classes("text-lg")

            def do_delete():
                resp = delete_layer(layer["layerid"])
                if resp and getattr(resp, "status_code", None) == 200:
                    ui.notify("✅ Изтрито успешно!")
                    refresh_table()
                    confirm.close()
                else:
                    try:
                        msg = resp.json().get("detail") if resp is not None else None
                    except Exception:
                        msg = None
                    ui.notify(f"❌ Грешка при изтриване! {msg or ''}")

            with ui.row().classes("justify-end gap-4 mt-4"):
                ui.button("Откажи", on_click=confirm.close)
                ui.button("🗑️ Изтрий", on_click=do_delete).classes("bg-red-500 text-white")
        confirm.open()

    # === Заглавие, бутони и филтри — вертикално вляво, таблица вдясно ===
    with ui.row().classes("w-full items-start no-wrap"):
        # 🧭 Ляв панел — 10%
        with ui.column().classes(
                "w-[5%] min-w-[180px] gap-2 p-2 bg-gray-50 rounded-xl shadow-md sticky top-2 h-[90vh] overflow-auto"
        ):
            ui.label("⛏️ Управление на пластове").classes("text-lg font-bold mb-2")

            ui.button("➕ Нов пласт", on_click=open_create_dialog).classes(
                "bg-blue-500 text-white w-full"
            )

            ui.separator().classes("my-2")

            ui.label("🔍 Филтриране по:").classes("text-md font-semibold mb-2")

            filter_name = ui.input("Име на пласт").props("clearable").classes("w-full")
            filter_type = ui.select(
                ["", "механичен", "контекст"], label="Тип пласт"
            ).classes("w-full")
            filter_color = ui.select(
                ["", "бял", "жълт", "охра", "червен", "сив", "тъмносив",
                    "кафяв", "светлокафяв", "тъмнокафяв", "черен"],
                label="Основен цвят",
            ).classes("w-full")

            ui.separator().classes("my-2")

            # ---Бутони под филтрите---
            ui.button("🎯 Приложи", on_click=lambda: refresh_table()).classes(
                "bg-green-600 text-white w-full"
            )

            with ui.row().classes("justify-between w-full"):
                def reset_filters():
                    filter_name.value = ''
                    filter_type.value = ''
                    filter_color.value = ''
                    refresh_table()

                ui.button("♻️ Нулирай", on_click=reset_filters).classes(
                    "bg-gray-400 text-white w-full"
                )

        # 📋 Таблица вдясно — 90%
        with ui.column().classes("w-[90%] p-1 overflow-auto"):
            table_container = ui.column().classes("w-full")

    # === Начално зареждане ===
    refresh_table()
