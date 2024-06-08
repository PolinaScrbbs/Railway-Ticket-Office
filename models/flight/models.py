from datetime import datetime, timedelta, timezone
from sqlalchemy import (Column, 
    Integer, DateTime, ForeignKey, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..train.models import Train

Base = declarative_base()

# Модель локаций
class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)

# Модель рейсов
class Flight(Base):
    __tablename__ = 'flights'
    
    id = Column(Integer, primary_key=True)
    where_from_id = Column(Integer, ForeignKey(Location.id), nullable=False)
    where_to_id = Column(Integer, ForeignKey(Location.id), nullable=False)
    train_id = Column(Integer, ForeignKey(Train.id), unique=True, nullable=False)
    departure_time = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=1), nullable=False)
    arrival_time = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=2), nullable=False)

    train = relationship(Train, foreign_keys=[train_id], back_populates='from_trains')
    from_location = relationship(Location, foreign_keys=[where_from_id], back_populates='from_flights')
    to_location = relationship(Location, foreign_keys=[where_to_id], back_populates='to_flights')
