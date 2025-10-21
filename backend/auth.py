# backend/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.users import models

# === Конфигурация ===
import os
from dotenv import load_dotenv

# Зареждаме променливите от .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-default-secret")  # fallback за локално
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

# === Помощни функции ===
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Създава JWT токен със срок на валидност."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# === Извличане на потребители ===
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        return None
    return user

# === Валидация на текущ потребител (от токен) ===
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалиден токен или липсваща автентикация.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
