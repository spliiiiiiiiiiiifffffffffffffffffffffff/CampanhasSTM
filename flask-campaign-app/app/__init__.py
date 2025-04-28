from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('instance.config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app