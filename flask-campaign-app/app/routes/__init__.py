from flask import Blueprint

# Importar os módulos de rota
from .auth_routes import auth_bp
from .campaign_routes import campaign_bp
from .gallery_routes import gallery_bp
from .association_routes import association_bp

# Registrar os blueprints
def register_routes(app):
    app.register_blueprint(auth_bp)  # Sem prefixo para que a rota '/' funcione
    app.register_blueprint(campaign_bp, url_prefix='/campaigns')
    app.register_blueprint(gallery_bp, url_prefix='/gallery')
    app.register_blueprint(association_bp, url_prefix='/associations')  # Certifique-se de que está registrado