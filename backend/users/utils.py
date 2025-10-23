from sqlalchemy.orm import Session
from . import crud, schemas

def ensure_admin_exists(db: Session):
    """Ако няма администратор в базата, създава се дефолтен"""
    admin = crud.get_user_by_username(db, "admin")
    if not admin:
        user_in = schemas.UserCreate(
            username="admin",
            email="admin@example.com",
            password="admin123"  # ⇐ смени след първо влизане!
        )
        db_admin = crud.create_user(db, user_in)
        db_admin.role = "admin"
        db.commit()
        print("✅ Създаден е администратор: admin / admin123")
    else:
        print("ℹ️ Администратор вече съществува.")


# backend/users/utils.py

import re
from fastapi import HTTPException

# Регулярно изражение за силна парола
PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)

def validate_password_strength(password: str):
    """
    Проверява силата на паролата.
    Изисквания:
      - Минимум 8 символа
      - Поне 1 главна буква
      - Поне 1 малка буква
      - Поне 1 цифра
      - Поне 1 специален символ (@$!%*?&)
    """
    if not PASSWORD_PATTERN.match(password):
        raise HTTPException(
            status_code=400,
            detail=(
                "Паролата трябва да съдържа поне 8 символа, "
                "една главна, една малка буква, една цифра и специален символ."
            )
        )

