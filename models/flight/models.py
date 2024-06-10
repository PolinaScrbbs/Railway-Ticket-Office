from datetime import datetime, timedelta, timezone
from sqlalchemy import (Column, Integer, DateTime, ForeignKey, String, Enum, CHAR, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum as BaseEnum

Base = declarative_base()

# Enum для типа поездов
class TrainType(BaseEnum):
    TRAIN = "Поезд"
    ELECTRIC_TRAIN = "Электричка"

# Модель локаций
class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)

    from_flights = relationship('Flight', back_populates='from_location', foreign_keys='Flight.where_from_id')
    to_flights = relationship('Flight', back_populates='to_location', foreign_keys='Flight.where_to_id')

# Модель поездов
class Train(Base):
    __tablename__ = 'train'

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

# Enum для типа вагонов
class CarriageType(BaseEnum):
    RESERVED_SEAT = "Плацкарт"
    COMPARTMENT = "Купе"
    FC = "Первый класс"
    LUXURY = "Люкс"
    SEDENTARY = "Сидячий"

# Таблица для связи вагонов и мест
carriage_seat_association = Table(
    'carriage_seat_association',
    Base.metadata,
    Column('carriage_id', Integer, ForeignKey('carriages.id'), primary_key=True),
    Column('seat_id', Integer, ForeignKey('seats.id'), primary_key=True)
)

# Модель вагонов
class Carriage(Base):
    __tablename__ = 'carriages'

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey(Train.id), nullable=False)
    type = Column(Enum(CarriageType), nullable=False)

    train = relationship('Train', back_populates='carriages')
    seats = relationship('Seat', secondary=carriage_seat_association, back_populates='carriages')

# Модель мест в вагонах
class Seat(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True)
    seat_number = Column(String, nullable=False)

    carriages = relationship('Carriage', secondary=carriage_seat_association, back_populates='seats')
