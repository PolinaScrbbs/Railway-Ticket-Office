from .models import User
from sqlalchemy.orm import Session

# Функция для регистрации пользователя
def register_user(session: Session, login: str, password: str, name: str, surname: str, patronymic: str):
    # Проверяем, не существует ли пользователь с таким же логином
    if session.query(User).filter_by(login=login).first():
        raise ValueError("User with this login already exists.")
    
    # Создаем нового пользователя
    user = User(login=login, name=name, surname=surname, patronymic=patronymic)
    user.password = password  # Устанавливаем пароль (он будет автоматически хеширован)
    
    session.add(user)
    session.commit()
    return user

def authenticate_user(session: Session, login: str, password: str) -> User:
    # Находим пользователя с указанным логином
    user = session.query(User).filter_by(login=login).first()
    
    # Проверяем, найден ли пользователь и соответствует ли введенный пароль хэшу его пароля в базе данных
    if not user or not user.verify_password(password):
        raise ValueError("Неправильный логин или пароль.")
    
    return user