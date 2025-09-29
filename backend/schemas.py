from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    username: str
    email: str
    role: Optional[str] = "user"


class UserLogin(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=4)


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=4)


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class PasswordChange(BaseModel):
    old_password: str
    new_password: constr(min_length=6)
