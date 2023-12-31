import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv(".env")


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    URL_FIREBASE_EVALUATION = os.environ.get('URL_FIREBASE_EVALUATION')
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
