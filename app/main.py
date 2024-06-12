from app.database import load_fixtures
from .fixtures import fixtures_data
from .forms.auth import LoginWindow

if __name__ == "__main__":
    load_fixtures(fixtures_data)
    registration_window = LoginWindow()
    registration_window.run()