from dotenv import load_dotenv
import os
import urllib.parse

os.environ.pop('DB_HOST', None)
os.environ.pop('DB_PORT', None)
os.environ.pop('DB_NAME', None)
os.environ.pop('DB_USER', None)
os.environ.pop('DB_PASS', None)
os.environ.pop('DATABASE_URL', None)

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Сформировать URL для SQLAlchemy
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL_ENCODED = urllib.parse.quote_plus(DATABASE_URL)
print(DATABASE_URL_ENCODED)
os.environ["DATABASE_URL"] = DATABASE_URL