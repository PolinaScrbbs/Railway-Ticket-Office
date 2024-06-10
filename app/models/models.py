import bcrypt
from sqlalchemy import VARCHAR, Column, Integer, String, Enum, DateTime, ForeignKey, Numeric, Boolean, CHAR, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as BaseEnum
from datetime import datetime, timedelta, timezone

from app.database import get_session

Base = declarative_base()

# Enum для типа локаций
class LocationType(BaseEnum):
    CITY = "Город"
    STATION = "Станция"

# Модель локаций
class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    type = Column(Enum(LocationType), nullable=False)

    from_flights = relationship('Flight', back_populates='from_location', foreign_keys='Flight.where_from_id')
    to_flights = relationship('Flight', back_populates='to_location', foreign_keys='Flight.where_to_id')

# Enum для типа поездов
class TrainType(BaseEnum):
    TRAIN = "Поезд"
    ELECTRIC_TRAIN = "Электричка"

# Модель поездов
class Train(Base):
    __tablename__ = 'trains'

    id = Column(Integer, primary_key=True)
    number = Column(CHAR(3), unique=True, nullable=False)
    type = Column(Enum(TrainType), nullable=False)

    carriages = relationship('Carriage', back_populates='train')
    flights = relationship('Flight', back_populates='train')

    def carriage_number(self):
        return len(self.carriages)

    def seats_number(self):
        return sum(len(carriage.seats) for carriage in self.carriages)

# Модель рейсов
class Flight(Base):
    __tablename__ = 'flights'
    
    id = Column(Integer, primary_key=True)
    where_from_id = Column(Integer, ForeignKey(Location.id), nullable=False)
    where_to_id = Column(Integer, ForeignKey(Location.id), nullable=False)
    train_id = Column(Integer, ForeignKey(Train.id), nullable=False)
    departure_time = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=1), nullable=False)
    arrival_time = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=2), nullable=False)

    train = relationship('Train', back_populates='flights')
    from_location = relationship('Location', back_populates='from_flights', foreign_keys=[where_from_id])
    to_location = relationship('Location', back_populates='to_flights', foreign_keys=[where_to_id])

    tickets = relationship('Ticket', back_populates='flight')

    @property
    def direction(self):
        return f"{self.from_location.title} - {self.to_location.title}"
    
    @property
    def travel_time(self):
        return f"{self.departure_time} - {self.arrival_time}"

# Enum для типа вагонов
class CarriageType(BaseEnum):
    RESERVED_SEAT = "Плацкарт"
    COMPARTMENT = "Купе"
    FC = "Первый класс"
    LUXURY = "Люкс"
    SEDENTARY = "Сидячий"

# # Таблица для связи вагонов и мест
# carriage_seat_association = Table(
#     'carriage_seat_association',
#     Base.metadata,
#     Column('carriage_id', Integer, ForeignKey('carriages.id')),
#     Column('seat_id', Integer, ForeignKey('seats.id'))
# )

# Модель вагонов
class Carriage(Base):
    __tablename__ = 'carriages'

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey(Train.id), nullable=False)
    number = Column(VARCHAR(2), nullable=False)
    type = Column(Enum(CarriageType), nullable=False)

    train = relationship('Train', back_populates='carriages')
    seats = relationship('Seat', back_populates='carriage')
    
    def get_type(self):
        return self.type.value

# Модель мест в вагонах
class Seat(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True)
    carriage_id = Column(Integer, ForeignKey(Carriage.id), nullable=False)
    number = Column(VARCHAR(3), nullable=False)

    tickets = relationship('Ticket', back_populates='seat')
    carriage = relationship("Carriage", back_populates="seats", foreign_keys=[carriage_id])

# Определение ролей с помощью перечислений
class Role(BaseEnum):
    ADMIN = "admin"
    USER = "user"

# Модель пользователей
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    patronymic = Column(String(20), nullable=False)

    reservations = relationship('Reservation', back_populates='user')

    @property
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

# Модель билетов
class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    seat_id = Column(Integer, ForeignKey(Seat.id), unique=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_round_trip = Column(Boolean, default=False, nullable=False) # В оба конца?

    flight = relationship('Flight', back_populates='tickets')
    seat = relationship('Seat', back_populates='tickets')
    reservation = relationship('Reservation', uselist=False, back_populates='ticket')

    @property
    def ticket_number(self):
        ticket_id = self.id
        formatted_id = f"{ticket_id:08}"
        return formatted_id

# Модель броней
class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    ticket = relationship('Ticket', back_populates='reservation')
    user = relationship('User', back_populates='reservations')


# User.reservations = relationship('Reservation', order_by=Reservation.id, back_populates='user')
# Flight.tickets = relationship('Ticket', order_by=Ticket.id, back_populates='flight')
# Seat.ticket = relationship('Ticket', uselist=False, back_populates='seat')
