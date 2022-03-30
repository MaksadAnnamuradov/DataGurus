from flask import Flask
from config import BaseConfig
from flask.helpers import get_root_path
from flask_login import login_required
from flask_mongoengine import MongoEngine
import dash
from flask_user import login_required, UserManager, UserMixin

def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)

    return server

def register_dashapps(app):
    from .dashApps import iris_kmeans, mongo_dash_datatable

    
    dashapp1 = iris_kmeans.init_dash(app)
    dashapp2 = mongo_dash_datatable.init_dash(app)


    _protect_dashviews(dashapp1)
    _protect_dashviews(dashapp2)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.routes_pathname_prefix):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func])



def register_extensions(server):
    from app.extensions import db
    from app.extensions import login
    from app.extensions import migrate

    #db.init_app(server)
    db = MongoEngine(server)
    login.init_app(server)
    login.login_view = 'auth.login'

     # Define the User document.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Document, UserMixin):
        active = db.BooleanField(default=True)

        # User authentication information
        username = db.StringField(default='')
        password = db.StringField()

        email = db.StringField()

        # User information
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')

        # Relationships
        roles = db.ListField(db.StringField(), default=[])

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(server, db, User)
    #migrate.init_app(server, db)
    

def register_blueprints(server):
    from app.main import main
    from app.auth import auth

    

    server.register_blueprint(main)
    server.register_blueprint(auth)
