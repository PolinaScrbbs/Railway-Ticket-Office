from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER



DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    return SessionLocal()

def load_fixtures(fixtures_data):
    session = get_session()

    print("Before insertion:")
    for model, data_list in fixtures_data.items():
        try:
            records = session.query(model).all()
            for record in records:
                print(f"Existing {model.__name__}: {record}")
        except Exception as e:
            print(f"Error querying the database before insertion for {model.__name__}: {e}")

        # Вставка начальных данных в таблицу для текущей модели
        for data in data_list:
            try:
                # Проверка на существование записи
                existing_record = session.query(model).filter_by(**data).first()
                if existing_record:
                    print(f"{model.__name__} with data {data} already exists, skipping.")
                else:
                    new_record = model(**data)
                    session.add(new_record)
                    print(f"Added {model.__name__}: {data}")
            except Exception as e:
                print(f"Error adding {model.__name__} with data {data}: {e}")
                continue

    try:
        session.commit()
        print("Initial data inserted.")
    except Exception as e:
        session.rollback()
        print(f"Error committing the session: {e}")

    print("After insertion:")
    for model, _ in fixtures_data.items():
        try:
            records = session.query(model).all()
            for record in records:
                print(f"{model.__name__}: {record}")
        except Exception as e:
            print(f"Error querying the database after insertion for {model.__name__}: {e}")

    session.close()

