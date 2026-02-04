from flask import Flask
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"
    app.config["DATABASE"] = "instance/dental.db"

    init_db(app)

    from .routes import main
    app.register_blueprint(main)

    return app
