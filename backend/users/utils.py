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
