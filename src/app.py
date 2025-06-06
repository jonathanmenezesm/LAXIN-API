from flask import Flask
from src.controller.usuario_controller import bp_usuarios 
from config import Config  # Importa a classe de configuração


def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)  # Carrega as configs do config.py
    
    app.register_blueprint(bp_usuarios)

    return app
