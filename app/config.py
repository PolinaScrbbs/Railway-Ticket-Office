from dotenv import load_dotenv
import os

os.environ.pop('DB_HOST', None)
os.environ.pop('DB_PORT', None)
os.environ.pop('DB_NAME', None)
os.environ.pop('DB_USER', None)
os.environ.pop('DB_PASS', None)

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

print(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)