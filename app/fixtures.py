from .models.models import Flight, LocationType, Seat, Ticket, Train, TrainType, Location

fixtures_data = {
    Train: [
        {"id": 1, "number": "001", "type": TrainType.TRAIN},
        {"id": 2, "number": "002", "type": TrainType.TRAIN}
    ],
    Location: [
        {"id": 1, "title": "Азербайджан", "type": LocationType.CITY},
        {"id": 2, "title": "Таджикистан", "type": LocationType.CITY},
        {"id": 3, "title": "Россия", "type": LocationType.CITY}
    ],
    Flight: [
        {"id": 1, "where_from_id": 3, "where_to_id": 1, "train_id": 1}
    ],
    Seat: [
        {"id": 1, "number": "1"}, {"id": 2, "number": "2"}, {"id": 3,"number": "3"}, {"id": 4, "number": "4"}, 
        {"id": 5, "number": "5"}, {"id": 6, "number": "6"}, {"id": 7, "number": "7"}, {"id": 8, "number": "8"},
    ],
    Ticket: [
        {"id": 1, "flight_id": 1, "seat_id": 1, "price": 2000.00}
    ]
}