"""Class-based Flask app configuration."""
# https://github.com/hackersandslackers/flask-blueprint-tutorial
from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Basic Configuration."""

    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_APP = "run.py"
    FLASK_PORT = environ.get("FLASK_PORT")

    # Flask-Assets
    # LESS_BIN = environ.get("LESS_BIN")
    # ASSETS_DEBUG = False
    # LESS_RUN_IN_DEBUG = False

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    # COMPRESSOR_DEBUG = False

# class TestingConfig(Config):
#     DB_SERVER = 'localhost'
#     # DEBUG = True
#     DATABASE_URI = 'sqlite:///:memory:'

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    CELERY_BROKER_URL = 'redis://192.168.99.100:6379/0'
    CELERY_RESULT_BACKEND = 'redis://192.168.99.100:6379/0'