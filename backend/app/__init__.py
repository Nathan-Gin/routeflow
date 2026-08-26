from flask import Flask, request
from app.routes import routes


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def home():
        return {"message": "Welcome to RouteFlow"}

    app.register_blueprint(routes)

    return app