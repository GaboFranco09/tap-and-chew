import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_HOST     = os.getenv('DB_HOST', '127.0.0.1')
    DB_PORT     = os.getenv('DB_PORT', '3306')
    DB_NAME     = os.getenv('DB_NAME', 'tapandchew_kitchen')
    DB_USER     = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )

    FIREBASE_DATABASE_URL      = os.getenv('FIREBASE_DATABASE_URL')
    FIREBASE_CREDENTIALS_PATH  = os.getenv('FIREBASE_CREDENTIALS_PATH')