from models.flight.models import Train, TrainType, Location
from models.user.models import User, Role

fixtures_data = {
    Train: [
        {"number": "002", "type": TrainType.TRAIN},
        {"number": "001", "type": TrainType.TRAIN}
    ],
    Location: [
        {"title": "Азербайджан"},
        {"title": "Таджикистан"},
        {"title": "Россия"}
    ],
    User: [
        {"login": "Азербайджан", "password_hash": "Азербайджан", "role": Role.USER,
          "name": "Азербайджан", "surname": "Азербайджан", "patronymic": "Азербайджан"}
    ]
}