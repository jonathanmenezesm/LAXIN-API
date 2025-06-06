from flask import Flask
from src.controller.usuario_controller import bp_usuarios

def create_app():
    
    app = Flask(__name__)
    app.register_blueprint(bp_usuarios)

    return app
