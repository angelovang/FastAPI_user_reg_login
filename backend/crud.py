from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    """Връща потребителя, ако username и password са валидни, иначе None"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not user.check_password(password):
        return None
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username,
                          email=user.email,
                          role="user")
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user: schemas.UserBase):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        if user.role:  # позволява промяна на role, ако е подадено
            db_user.role = user.role
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
