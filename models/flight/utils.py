from .models import Flight
from ..train.models import Train

def get_all_flights(session):
    # Получаем все рейсы и возвращаем их в виде списка
    flights = session.query(Flight).all()

    # Закрываем сессию
    session.close()

    return flights