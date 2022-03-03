from flask import Flask
from config import BaseConfig
from flask.helpers import get_root_path
from flask_login import login_required
import dash


def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)

    return server

def register_dashapps(app):
    from .dash import iris_kmeans, file_uploader

    
    dashapp1 = iris_kmeans.init_dash(app)
    dashapp2 = file_uploader.init_dash(app)

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

    db.init_app(server)
    login.init_app(server)
    login.login_view = 'auth.login'
    migrate.init_app(server, db)
    

def register_blueprints(server):
    from app.main import main
    from app.auth import auth
    server.register_blueprint(main)
    server.register_blueprint(auth)
