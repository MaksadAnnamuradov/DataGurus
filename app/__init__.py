from flask import Flask

def init_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")
    with app.app_context():
        from . import routes
        from .dash import demo, iris_kmeans

        app = demo.init_dash(app)
        app = iris_kmeans.init_dash(app)
    return app

