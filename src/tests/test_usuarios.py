import pytest
from flask import Flask
from src.controller.usuario_controller import bp_usuarios  # Ajuste o caminho conforme necessário
import src.database.usuarios_db as db  # Importando o módulo diretamente

app = Flask(__name__)
app.register_blueprint(bp_usuarios)

@pytest.fixture
def client():
    return app.test_client()

# Testando a rota de listagem de usuários (GET /usuarios/)
def test_listar_usuarios(client):
    resposta = client.get('/usuarios/')
    assert resposta.status_code == 200
    assert isinstance(resposta.json, list)  # Verifica se a resposta é uma lista
    
# Testando a rota de cadastro de usuário (POST /usuarios/cadastrar)
def test_cadastrar_usuario(client):
    db.usuarios.clear()  # Limpa a lista antes do teste

    novo_usuario = {
        "nome": "Teste",
        "sobrenome": "Usuário",
        "data_nascimento": "2000-01-01",
        "cpf": "12345678901",
        "celular": "11999999999",
        "email": "teste@email.com",
        "senha": "senha123"
    }

    resposta = client.post('/usuarios/cadastrar', json=novo_usuario)
    assert resposta.status_code == 201
    assert resposta.json["resposta"] == "Usuário cadastrado com sucesso!"

# Testando a busca de usuário por ID (GET /usuarios/<id>)
def test_obter_usuario(client):
    db.usuarios.clear()
    
    # Criando um usuário para testar a busca
    novo_usuario = {
        "nome": "Teste",
        "sobrenome": "Usuário",
        "data_nascimento": "2000-01-01",
        "cpf": "12345678902",
        "celular": "11999999999",
        "email": "teste@email.com",
        "senha": "senha123"
    }
    client.post('/usuarios/cadastrar', json=novo_usuario)

    resposta = client.get('/usuarios/1')  # Buscando pelo ID 1
    assert resposta.status_code == 200
    assert resposta.json["nome"] == "Teste"

# Testando a atualização de usuário por ID (PUT /usuarios/atualizar/<id>)
def test_atualizar_usuario(client):
    db.usuarios.clear()
    
    # Criando um usuário para testar a atualização
    novo_usuario = {
        "nome": "Teste",
        "sobrenome": "Usuário",
        "data_nascimento": "2000-01-01",
        "cpf": "12345678903",
        "celular": "11999999999",
        "email": "teste@email.com",
        "senha": "senha123"
    }
    client.post('/usuarios/cadastrar', json=novo_usuario)

    dados_atualizados = {
        "nome": "Teste Atualizado",
        "email": "novo@email.com"
    }
    resposta = client.put('/usuarios/atualizar/1', json=dados_atualizados)
    assert resposta.status_code == 200
    assert resposta.json["resposta"] == "Atualizado com sucesso"

# Testando a remoção de usuário por ID (DELETE /usuarios/remover/<id>)
def test_remover_usuario(client):
    db.usuarios.clear()
    
    # Criando um usuário para testar a remoção
    novo_usuario = {
        "nome": "Teste",
        "sobrenome": "Usuário",
        "data_nascimento": "2000-01-01",
        "cpf": "12345678904",
        "celular": "11999999999",
        "email": "teste@email.com",
        "senha": "senha123"
    }
    client.post('/usuarios/cadastrar', json=novo_usuario)

    resposta = client.delete('/usuarios/remover/1')
    assert resposta.status_code == 200
    assert resposta.json["resposta"] == "Usuário removido com sucesso!"