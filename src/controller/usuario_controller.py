from flask import Blueprint, request, jsonify
from sqlalchemy import select
# from database import usuarios_db #Linha de importação do db fake
# from src.database.usuarios_db import usuarios #Linha de importação do db fake
from src.model.usuario_model import Usuario
from src.model import db

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

# >>>>>>     Listar todos os usuarios (PAINEL ADMIN)
@bp_usuarios.route('/', methods=['GET'])
def listar_usuarios():
    stmt = db.select(Usuario)
    usuarios = db.session.scalars(stmt).all()
    usuarios_dict = [u.to_dict() for u in usuarios]
    return jsonify(usuarios_dict)

# >>>>>>     Crud - Cadastrar novo usuário
@bp_usuarios.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    dados_requisicao = request.get_json()
    
    if not dados_requisicao:
        return jsonify({'Erro': 'Todos os campos devem ser preenchidos'}), 400
    
    # Lista de campos obrigatórios
    campos_obrigatorios = ['nome', 'sobrenome', 'data_nascimento', 'cpf', 'celular', 'email', 'senha']

    # Verifica se todos os campos obrigatórios estão presentes e não vazios
    for campo in campos_obrigatorios:
        if campo not in dados_requisicao or not dados_requisicao[campo]:
            return jsonify({'Erro': f'O campo "{campo}" é obrigatório.'}), 400
        
    # Verifica se o CPF já está cadastrado
    usuario_existente = db.session.execute(
    select(Usuario).where(Usuario.cpf == dados_requisicao['cpf'])
    ).scalar_one_or_none()
    if usuario_existente:
        return jsonify({'Erro': 'CPF já cadastrado.'}), 400
    
    # Verifica se o celular já está cadastrado
    celular_existente = db.session.execute(
        select(Usuario).where(Usuario.celular == dados_requisicao['celular'])
    ).scalar_one_or_none()
    if celular_existente:
        return jsonify({'Erro': 'Celular já cadastrado.'}), 400
    
    # Verifica se o email já está cadastrado
    email_existente = db.session.execute(
        select(Usuario).where(Usuario.email == dados_requisicao['email'])
    ).scalar_one_or_none()
    if email_existente:
        return jsonify({'Erro': 'Email já cadastrado.'}), 400

    # Cria uma nova instância de Usuario com os dados da requisição enviada no body
    novo_usuario = Usuario(
        nome=dados_requisicao['nome'],
        sobrenome=dados_requisicao['sobrenome'],
        data_nascimento=dados_requisicao['data_nascimento'],
        cpf=dados_requisicao['cpf'],
        celular=dados_requisicao['celular'],
        email=dados_requisicao['email'],
        senha=dados_requisicao['senha'],
        role='user'
    )

    # INSERT INTO tb_usuario (nome,sobrenome,data_nascimento,cpf,celular,email,senha) VALUES ()
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'resposta': 'Usuário cadastrado com sucesso!'}), 201

# >>>>>>    cRud - Obter usuário por ID
@bp_usuarios.route('/<int:id_usuario>', methods=['GET'])
def obter_usuario(id_usuario):
    # Selecionar um registro específico
    stmt = select(Usuario).where(Usuario.id == id_usuario)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'Erro': 'Usuário não encontrado'}), 404

# >>>>>>    crUd - Atualizar usuário por ID
@bp_usuarios.route('/atualizar/<int:id_usuario>', methods=['PUT'])
def atualizar_usuario(id_usuario):
    dados_requisicao = request.get_json()

    if not dados_requisicao:
        return jsonify({'Erro': 'Nenhum dado enviado para atualização.'}), 400

    usuario_selecionado = db.session.execute(
        select(Usuario).where(Usuario.id == id_usuario)
    ).scalar_one_or_none()

    if not usuario_selecionado:
        return jsonify({'Erro': 'Usuário não encontrado'}), 404

    # Verificações de unicidade, onde garantimos que o CPF, email e celular que o usuário está tentando atualizar não sejam duplicados
    if 'cpf' in dados_requisicao and dados_requisicao['cpf'] != usuario_selecionado.cpf:
        cpf_existente = db.session.execute(
            select(Usuario).where(Usuario.cpf == dados_requisicao['cpf'])
        ).scalar_one_or_none()
        if cpf_existente:
            return jsonify({'Erro': 'CPF já cadastrado.'}), 400

    if 'email' in dados_requisicao and dados_requisicao['email'] != usuario_selecionado.email:
        email_existente = db.session.execute(
            select(Usuario).where(Usuario.email == dados_requisicao['email'])
        ).scalar_one_or_none()
        if email_existente:
            return jsonify({'Erro': 'Email já cadastrado.'}), 400

    if 'celular' in dados_requisicao and dados_requisicao['celular'] != usuario_selecionado.celular:
        celular_existente = db.session.execute(
            select(Usuario).where(Usuario.celular == dados_requisicao['celular'])
        ).scalar_one_or_none()
        if celular_existente:
            return jsonify({'Erro': 'Celular já cadastrado.'}), 400

    # Lista de campos permitidos para atualização
    campos_permitidos = {'nome', 'sobrenome', 'data_nascimento', 'cpf', 'celular', 'email', 'senha', 'role'}

    for campo in campos_permitidos:
        if campo in dados_requisicao:
            setattr(usuario_selecionado, campo, dados_requisicao[campo])

    db.session.commit()
    return jsonify({'resposta': 'Usuário atualizado com sucesso!'}), 200

# >>>>>>     cruD - Remover usuário por ID
@bp_usuarios.route('/remover/<int:id_usuario>', methods=['DELETE'])
def remover_usuario(id_usuario):

    user = db.session.execute(
        select(Usuario).where(Usuario.id == id_usuario)
    ).scalar_one_or_none()

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'resposta': 'Usuário removido com sucesso!'}), 200

    return jsonify({'Erro': 'Usuário não encontrado'}), 404


# >>>>>>    Adicionando a Blueprint de Login
@bp_usuarios.route('/login', methods=['POST'])
def Login():
    dados_requisicao = request.get_json()
    
    email = dados_requisicao.get('email')
    senha = dados_requisicao.get('senha')
    
    if not email or not senha:
        return jsonify({'mensagem': 'Todos os campos devem ser preenchidos!'}), 400
    
    usuario = db.session.execute(db.select(Usuario).where(Usuario.email == email)).scalar()
    
    if not usuario:
        return jsonify({'mensagem': 'Email ou senha estão incorretos.'}), 401
    
    if not usuario or usuario.senha != senha:
        return jsonify({'mensagem': 'Email ou senha estão incorretos.'}), 401
    
    # Retorne o nome do usuário junto com a mensagem de sucesso
    return jsonify({
        'mensagem': 'Usuário logado com sucesso!',
        'nome': usuario.nome,
        'id': usuario.id,
        'role': usuario.role
    }), 200