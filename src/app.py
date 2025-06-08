from flask import Flask
from src.controller.usuario_controller import bp_usuarios 
from config import Config  # Importa a classe de configuração
from src.model import db


def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)  # Carrega as configs do config.py

    db.init_app(app)  # Inicializa o banco de dados com a aplicação
    
    # Cria o banco de dados e as tabelas, se não existirem
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados

    app.register_blueprint(bp_usuarios)  # Registra o blueprint de usuários

    return app
