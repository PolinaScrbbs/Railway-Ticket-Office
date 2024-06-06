from datetime import datetime, timezone
from sqlalchemy import (Boolean, Column, 
    Integer, DateTime, ForeignKey, Numeric)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


from ..user.models import User
from ..flight.models import Flight
from ..train.models import Seat

Base = declarative_base()

# Модель билетов
class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    seat_id = Column(Integer, ForeignKey(Seat.id), unique=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_round_trip = Column(Boolean, default=False, nullable=False) # В оба конца?

    flight = relationship('Flight', back_populates='tickets')
    seat = relationship('Seat', back_populates='ticket')
    reservation = relationship('Reservation', uselist=False, back_populates='ticket')

# Модель броней
class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    ticket = relationship('Ticket', back_populates='reservation')
    user = relationship('User', back_populates='reservations')


User.reservations = relationship('Reservation', order_by=Reservation.id, back_populates='user')
Flight.tickets = relationship('Ticket', order_by=Ticket.id, back_populates='flight')
Seat.ticket = relationship('Ticket', uselist=False, back_populates='seat')