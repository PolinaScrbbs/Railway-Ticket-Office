from datetime import datetime, timedelta
from .models import Flight, Reservation, Ticket
from sqlalchemy.orm import joinedload
from sqlalchemy import not_

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

def get_available_tickets(session, flight_id):
    all_tickets = get_flight_tickets(session, flight_id)
    reserved_ticket_ids = [reservation.ticket_id for reservation in session.query(Reservation).all()]
    available_tickets = [ticket for ticket in all_tickets if ticket.id not in reserved_ticket_ids]

    return available_tickets

def create_reservation(session, ticket_id, user_id):
    reservation = Reservation(ticket_id=ticket_id, user_id=user_id)

    session.add(reservation)
    session.commit()

def get_reservations(session):
    one_month_ago = datetime.now() - timedelta(days=30)

    reservations = session.query(Reservation).filter(Reservation.date >= one_month_ago).all()
    return reservations

def get_user_reservations(session, user_id):
    user_reservations = session.query(Reservation).filter(Reservation.user_id == user_id).all()
    return user_reservations