import pytest
from flask import Flask
from src.controller.usuario_controller import bp_usuarios
import src.database.usuarios_db as db

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bp_usuarios)
    return app.test_client()

@pytest.fixture
def reset_db():
    """Reseta a lista de usuários antes de cada teste."""
    db.usuarios.clear()