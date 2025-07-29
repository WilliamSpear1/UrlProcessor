from flask import Flask

from UrlProcessor.URLProcessor.routes import bp


def create_app() -> Flask:
        flask_app = Flask(__name__)
        flask_app.register_blueprint(blueprint=bp)
        return flask_app

app = create_app()