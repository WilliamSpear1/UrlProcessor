from flask import Flask
from URLProcessor.routes import bp

def create_app():
        flask_app = Flask(__name__)
        flask_app.register_blueprint(blueprint=bp)
        return flask_app

app = create_app()