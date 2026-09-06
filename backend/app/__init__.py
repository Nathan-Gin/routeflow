from flask import Flask, send_from_directory
from app.routes import routes
from pathlib import Path


def create_app():
    app = Flask(__name__)

    app.register_blueprint(routes)

    frontend_path = Path(__file__).resolve().parents[2] / "frontend"

    @app.get("/")
    def home():
        return send_from_directory(frontend_path, "index.html")

    """When the broswer searches
    for a path e.g styles.css it will automatically
    search the current directory this ensures we instead
    when sending get requests our route tells us to
    look in the /frontend directory
    """
    @app.get("/<path:filename>")
    def frontend_files(filename):
        return send_from_directory(frontend_path, filename)

    return app