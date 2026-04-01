import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

load_dotenv()

_initialized = False


def init_firebase():
    global _initialized
    if not _initialized:
        cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
        db_url    = os.getenv('FIREBASE_DATABASE_URL')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {'databaseURL': db_url})
        _initialized = True


def get_db():
    init_firebase()
    return db