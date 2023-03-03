from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    
    # creating the flask object
    app = Flask(__name__)

    # configuring app:
    app.config.from_object("config.app_config")

    db.init_app(app)


    from commands import db

    @app.route("/")
    def hello():
        return {"message" : "Welcome to my project"}

    return app