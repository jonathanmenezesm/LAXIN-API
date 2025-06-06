from flask import Blueprint, request, jsonify
from src.database.usuarios_db import usuarios

'''
Rotas para gerenciamento de usuários:

- Create (POST)   : /usuarios/                - Criar novo usuário
- Read   (GET)    : /usuarios/                - Listar todos os usuários
- Read   (GET)    : /usuarios/<int:user_id>   - Obter usuário por ID
- Update (PUT)    : /usuarios/<int:user_id>   - Atualizar usuário por ID
- Delete (DELETE) : /usuarios/<int:user_id>   - Remover usuário por ID
'''



# Definindo o Blueprint para usuários
bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# cRud Listar todos os usuarios (PAINEL ADMIN)
@bp_usuarios.route('/', methods=['GET'])
def listar_usuarios():
    # Aqui você implementaria a lógica para listar usuários
    return jsonify(usuarios)


# Crud - Cadastrar novo usuário
@bp_usuarios.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    dados_requisicao = request.get_json()
    
    novo_usuario = {
        'id': len(usuarios) + 1,  # Gerando um novo ID baseado no tamanho da lista
        'nome': dados_requisicao['nome'],
        'sobrenome': dados_requisicao['sobrenome'],
        'data_nascimento': dados_requisicao['data-nascimento'],
        'cpf': dados_requisicao['cpf'],
        'celular': dados_requisicao['celular'],
        'email': dados_requisicao['email'],
        'senha': dados_requisicao['senha']
    }
    usuarios.append(novo_usuario)
    return jsonify({'resposta': 'Usuário cadastrado com sucesso!'}), 201


