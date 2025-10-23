import re
from nicegui import ui

PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)

def validate_password_frontend(password: str) -> bool:
    """Локална проверка преди заявка към сървъра."""
    if not PASSWORD_PATTERN.match(password):
        ui.notify(
            "⚠️ Паролата трябва да съдържа поне 8 символа, "
            "една главна, една малка буква, една цифра и специален символ.",
            color="warning"
        )
        return False
    return True


'''
Да се интегрира преди продукция !!!

------------Пример в frontend/users/pages.py (регистрация):----------

from frontend.common.password_utils import validate_password_frontend

def validate_and_register():
    if not validate_password_frontend(password.value):
        return
    response = register_user(username.value, email.value, password.value)

----------Пример в frontend/users/dashboard.py (смяна на парола):-----

from frontend.common.password_utils import validate_password_frontend

def change_password_action():
    if not validate_password_frontend(new_password.value):
        return
    # ... останалия код

'''