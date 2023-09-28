"""Service config"""
import os

if not os.path.exists("db/"):
    os.makedirs("db/")

DATABASE_URL = os.environ.get("DATABASE_URI", "sqlite:///db/app.sqlite")
HOLIDAY_HOST = os.environ.get("HOLIDAY_HOST", "http://holiday:8000/")
SCHDULER_HOST = os.environ.get("SCHDULER_HOST", "http://scheduler:8001/")
