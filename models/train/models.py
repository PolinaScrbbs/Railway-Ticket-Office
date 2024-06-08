from sqlalchemy import (Column, 
    Integer, ForeignKey, Enum, CHAR, String, Table)
from enum import Enum as BaseEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class TrainType(BaseEnum):
    TRAIN = "Поезд"
    ELECTRIC_TRAIN = "Электричка"

# Модель поездов
class Train(Base):
    __tablename__ = 'train'

    id = Column(Integer, primary_key=True)
    number = Column(CHAR(3), unique=True, nullable=False)
    type = Column(Enum(TrainType), nullable=False)

    carriages = relationship('Carriage', back_populates='train')

    def carriage_number(self):
        return len(self.carriages)

    def seats_number(self):
        return sum(len(carriage.seats) for carriage in self.carriages)

class CarriageType(BaseEnum):
    RESERVED_SEAT = "Плацкарт"
    COMPARTMENT = "Купе"
    FC = "Первый класс"
    LUXURY = "Люкс"
    SEDENTARY = "Сидячий"

# Таблица содержащая места вагона
carriage_seat_association = Table(
    'carriage_seat_association',
    Base.metadata,
    Column('carriage_id', Integer, ForeignKey('carriages.id'), primary_key=True),
    Column('seat_id', Integer, ForeignKey('seats.id'), primary_key=True, unique=True)
)

# Модель вагонов
class Carriage(Base):
    __tablename__ = 'carriages'

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey(Train.id), nullable=False)
    type = Column(Enum(CarriageType), nullable=False)

    train = relationship('Train', back_populates='carriages')
    seats = relationship('Seat', secondary=carriage_seat_association, back_populates='carriages')

# Модель места в вагоне
class Seat(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True)
    seat_number = Column(String, nullable=False)

    carriages = relationship('Carriage', secondary=carriage_seat_association, back_populates='seats')
    