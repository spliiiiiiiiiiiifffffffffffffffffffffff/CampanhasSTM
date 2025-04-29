from flask import Flask
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Registrar rotas
    register_routes(app)

    return app