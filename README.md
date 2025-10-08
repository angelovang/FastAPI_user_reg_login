Стурктора на проекта :

backend/
├── archaeology/
│   ├── models.py      # Tbllayer модел за SQLite с CheckConstraint
│   ├── schemas.py     # Pydantic схеми за Tbllayer
│   ├── crud.py        # CRUD функции за Tbllayer
│   └── router.py      # API endpoints за археология
│
├── users/
│   ├── models.py      # User модел
│   ├── schemas.py     # Pydantic схеми за User
│   ├── crud.py        # CRUD функции и логика за authentication
│   ├── router.py      # API endpoints за потребители (login, CRUD, change password)
│   └── utils.py       # ensure_admin_exists (startup helper)
│
├── database.py        # Engine, SessionLocal, Base и get_db
├── auth.py            # create_access_token и auth логика
├── main.py            # Стартира FastAPI, регистрира routers и стартира startup event
└── dependencies.py    # Общи зависимости (по избор)


frontend/
├── app.py                    # основна точка за стартиране
├── common/
│   ├── __init__.py
│   ├── layout.py             # navbar-и, header-и, общи UI компоненти
│   ├── session.py            # глобална сесия, helpers като get_session(), logout()
│   └── api.py                # общи функции за HTTP заявки към бекенда
├── users/
│   ├── __init__.py
│   ├── pages.py              # login, register, dashboard
│   ├── api.py                # специфични user API функции
│   └── components.py         # диалози, таблици, дребни UI елементи
└── archaeology/
    ├── __init__.py
    ├── pages.py              # страници за пластове, примеси, фрагменти и пр.
    ├── api.py                # CRUD функции към backend archaeology endpoints
    └── components.py         # общи UI елементи (dropdowns, таблици)
