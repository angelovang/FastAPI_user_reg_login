from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    username: str
    email: str

#class UserLogin(BaseModel):
#    username: str
#    password: str

class UserLogin(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=4)

#class UserCreate(UserBase):
#    password: str
class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=4)


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
