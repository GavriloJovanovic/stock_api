# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # SQLite DB configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import models so that create_all() works
    from . import models
    with app.app_context():
        db.create_all()

    # Register routes
    from .routes import stock_bp
    app.register_blueprint(stock_bp, url_prefix="/")

    return app

