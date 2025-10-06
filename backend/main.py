from fastapi import FastAPI
from sqlalchemy.orm import Session
from backend.database import Base, engine, SessionLocal
from backend.users.router import router as users_router
from backend.archaeology.router import router as archaeology_router
from backend.users.utils import ensure_admin_exists

# ---- Създаване на таблиците ----
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ---- Регистрация на routers ----
app.include_router(users_router)
app.include_router(archaeology_router)

# ---- Startup event ----
@app.on_event("startup")
def startup():
    db: Session = SessionLocal()
    try:
        ensure_admin_exists(db)
    finally:
        db.close()
