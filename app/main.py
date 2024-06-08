from app.database import load_fixtures
from .fixtures import fixtures_data
from .forms.auth import RegistrationWindow

if __name__ == "__main__":
    load_fixtures(fixtures_data)
    registration_window = RegistrationWindow()
    registration_window.run()