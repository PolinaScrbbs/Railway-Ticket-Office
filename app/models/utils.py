from .models import Flight, Ticket
from sqlalchemy.orm import joinedload

from .models import User
from sqlalchemy.orm import Session

def register_user(session: Session, login: str, password: str, name: str, surname: str, patronymic: str):
    if session.query(User).filter_by(login=login).first():
        raise ValueError("User with this login already exists.")
    
    user = User(login=login, name=name, surname=surname, patronymic=patronymic)
    user.password = password
    
    session.add(user)
    session.commit()
    return user

def authenticate_user(session: Session, login: str, password: str) -> User:
    user = session.query(User).filter_by(login=login).first()
    
    if not user or not user.verify_password(password):
        raise ValueError("Неправильный логин или пароль.")
    
    return user

def get_all_flights(session):
    return session.query(Flight).options(
        joinedload(Flight.from_location),
        joinedload(Flight.to_location),
        joinedload(Flight.train)
    ).all()

def get_flight_tickets(session, flight_id):
    return session.query(Ticket).options(
        joinedload(Ticket.flight),
        joinedload(Ticket.seat)
    ).filter_by(flight_id=flight_id).all()