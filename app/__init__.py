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
    from app.dashapp1.layout import layout
    from app.dashapp1.callbacks import register_callbacks

    from app.animal_calls.layout import animal_layout
    from app.animal_calls.callbacks import register_animal_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp1 = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                         meta_tags=[meta_viewport])
    dashapp2 = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/animal/',
                         assets_folder=get_root_path(__name__) + '/animal/assets/',
                         meta_tags=[meta_viewport])

    with app.app_context():
        dashapp1.title = 'Dashapp 1'
        dashapp1.layout = layout
        register_callbacks(dashapp1)
    
    with app.app_context():
        dashapp2.title = 'Dashapp 2'
        dashapp2.layout = animal_layout
        register_animal_callbacks(dashapp2)

    _protect_dashviews(dashapp1)
    _protect_dashviews(dashapp2)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
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
