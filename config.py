import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SESSION_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_URL = os.getenv("DATABASE_URL") 
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
    else:
        DATABASE_URL = 'sqlite:///voyage.db'

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    PORT = os.getenv("PORT")