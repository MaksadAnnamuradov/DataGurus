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
    USER_APP_NAME = "DataGurus"      # Shown in and email templates and page footers
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form
    USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
    USER_ENABLE_CHANGE_USERNAME = True  # Allow users to change their username
    USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
    USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
    USER_ENABLE_EMAIL = True  # Register with Email
    USER_ENABLE_REGISTRATION = True  # Allow new users to register



        # Flask-Mail settings
    # For smtp.gmail.com to work, you MUST set "Allow less secure apps" to ON in Google Accounts.
    # Change it in https://myaccount.google.com/security#connectedapps (near the bottom).
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'd6d92e530b4a3b'
    MAIL_PASSWORD = '409f126ee39a44'
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@data-gurus.com>'

    # Sendgrid settings
    SENDGRID_API_KEY='place-your-sendgrid-api-key-here'

    # Flask-User settings
    USER_EMAIL_SENDER_NAME = 'Maksad'
    USER_EMAIL_SENDER_EMAIL = 'maksad.annamuradow98@gmail.com'

