import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI", "sqlite:///posts.db")
    REMEMBER_COOKIE_DURATION = timedelta(days=7)