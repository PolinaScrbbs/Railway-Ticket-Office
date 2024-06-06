import bcrypt
from sqlalchemy import (Column, 
    Integer, String, Enum)
from enum import Enum as BaseEnum
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

#Определение ролей с помощью перечислений
class Role(BaseEnum):

    ADMIN = "admin"
    USER = "user"

#Модель пользователей
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    patronymic = Column(String(20), nullable=False)

    def full_name(self):
        return f'{self.name} {self.surname} {self.patronymic}'

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))