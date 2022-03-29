"""Flask config."""
from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

import os


def get_sqlite_uri():
    basedir = os.path.abspath(os.path.dirname(__file__))
    #db_name = os.environ['sqlite:///${PWD}/app.db'].split('/')[-1]
    return f'sqlite:///{basedir}/app.db'
    
class BaseConfig:
    """Flask configuration variables."""

    # General Config
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Assets
    LESS_BIN = environ.get("LESS_BIN")
    ASSETS_DEBUG = environ.get("ASSETS_DEBUG")
    LESS_RUN_IN_DEBUG = environ.get("LESS_RUN_IN_DEBUG")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = environ.get("COMPRESSOR_DEBUG")

    SQLALCHEMY_DATABASE_URI = get_sqlite_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key_change_as_you_wish_make_it_long_123'

    # Flask-MongoEngine settings
    MONGODB_SETTINGS = {
        'db': 'user_db',
        'host': "mongodb+srv://dash:Dash1234@cluster0.jipdo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    }

      # Flask-User settings
    USER_APP_NAME = "Flask-User MongoDB App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form

