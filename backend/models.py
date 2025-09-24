from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from .database import Base

class User(Base):
    __tablename__ = "tblregistered"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

