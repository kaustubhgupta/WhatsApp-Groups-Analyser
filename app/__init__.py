from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    with app.app_context():
        from app import views

    return app
