from flask import Flask
from flask_cors import CORS
from app.register import register
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    register_extensions(app)
    register(app)
    return app 

def register_extensions(app):
    from bootstrap.extensions import db, login
    db.init_app(app)
    # login.init_app(app)


app = create_app()