from flask import Blueprint, request, jsonify
from src.database.usuarios_db import usuarios

'''
Rotas para gerenciamento de usuários:

- OK Create (POST)   : /usuarios/                - Criar novo usuário
- OK Read   (GET)    : /usuarios/                - Listar todos os usuários (PAINEL ADMIN)
- OK Read   (GET)    : /usuarios/<int:id_usuario>   - Obter usuário por ID
- OK Update (PUT)    : /usuarios/<int:id_usuario>   - Atualizar usuário por ID
- OK Delete (DELETE) : /usuarios/<int:id_usuario>   - Remover usuário por ID
'''


# Definindo o Blueprint para usuários
bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Listar todos os usuarios (PAINEL ADMIN)
@bp_usuarios.route('/', methods=['GET'])
def listar_usuarios():
    # Aqui você implementaria a lógica para listar usuários
    return jsonify(usuarios)


# Crud - Cadastrar novo usuário
@bp_usuarios.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    dados_requisicao = request.get_json()
    
        # Lista de campos obrigatórios
    campos_obrigatorios = ['nome', 'sobrenome', 'data-nascimento', 'cpf', 'celular', 'email', 'senha']

    # Verifica se todos os campos obrigatórios estão presentes e não vazios
    for campo in campos_obrigatorios:
        if campo not in dados_requisicao or not dados_requisicao[campo]:
            return jsonify({'Erro': f'O campo "{campo}" é obrigatório.'}), 400
        
    # Verifica se o CPF já está cadastrado
    for usuario in usuarios:
        if usuario['cpf'] == dados_requisicao['cpf']:
            return jsonify({'Erro': 'CPF já cadastrado.'}), 400

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

# cRud - Obter usuário por ID
@bp_usuarios.route('/<int:id_usuario>', methods=['GET'])
def obter_usuario(id_usuario):
    for usuario in usuarios:
        if usuario['id'] == id_usuario:
            return jsonify(usuario), 200
    return jsonify({'Erro': 'Usuário não encontrado'}), 404

# crUd - Atualizar usuário por ID
@bp_usuarios.route('/atualizar/<int:id_usuario>', methods=['PUT'])
def atualizar_usuario(id_usuario):
    dados_requisicao = request.get_json()
    if not dados_requisicao:
        return jsonify({'Erro': 'Todos os campos devem ser preenchidos'}), 400

    campos_permitidos = {'nome', 'sobrenome', 'data-nascimento', 'cpf', 'celular', 'email', 'senha'}

    for usuario in usuarios:
        if usuario['id'] == id_usuario:
            for campo in campos_permitidos:
                if campo in dados_requisicao:
                    usuario[campo] = dados_requisicao[campo]
            return jsonify({'resposta': 'Atualizado com sucesso'}), 200

    return jsonify({'Erro': 'Usuário não encontrado'}), 404

# cruD - Remover usuário por ID
@bp_usuarios.route('/remover/<int:id_usuario>', methods=['DELETE'])
def remover_usuario(id_usuario):
    dados_requisicao = request.get_json()

    for usuario in usuarios:
        if usuario['id'] == id_usuario:
            usuarios.remove(usuario)
            return jsonify({'resposta': 'Usuário removido com sucesso!'}), 200

    return jsonify({'Erro': 'Usuário não encontrado'}), 404
