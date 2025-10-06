from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from . import crud, schemas
from backend.auth import create_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# ---------------- LOGIN ----------------
@router.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="❌ Невалидно потребителско име или парола")

    access_token = create_access_token(data={"sub": db_user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.username,
        "id": db_user.id,
        "role": db_user.role
    }

# ---------------- CREATE ----------------
@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# ---------------- READ ALL ----------------
@router.get("/", response_model=List[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

# ---------------- UPDATE ----------------
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id=user_id, user=user)

# ---------------- DELETE ----------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id=user_id)

# ---------------- CHANGE PASSWORD ----------------
@router.put("/{user_id}/change-password")
def change_password(user_id: int, passwords: schemas.PasswordChange, db: Session = Depends(get_db)):
    db_user = db.query(crud.models.User).filter(crud.models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Потребителят не е намерен")

    if not db_user.check_password(passwords.old_password):
        raise HTTPException(status_code=400, detail="Старият парола е грешна")

    db_user.set_password(passwords.new_password)
    db.commit()
    db.refresh(db_user)
    return {"msg": "Паролата е променена успешно"}
