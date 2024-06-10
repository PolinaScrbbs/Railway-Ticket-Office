from .models import Flight, Train
from sqlalchemy.orm import joinedload

def get_all_flights(session):
    return session.query(Flight).options(
        joinedload(Flight.from_location),
        joinedload(Flight.to_location),
        joinedload(Flight.train)
    ).all()