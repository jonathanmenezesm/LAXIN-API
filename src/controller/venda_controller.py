from flask import Blueprint, request, jsonify
from sqlalchemy import select
from src.model.venda_model import Venda
from src.model.usuario_model import Usuario
from src.model import db
from datetime import datetime

'''
Rotas para gerenciamento de vendas:

- OK Create (POST)   : /vendas/                - Criar nova venda
- OK Read   (GET)    : /vendas/                - Listar todas as vendas (PAINEL ADMIN)
- OK Read   (GET)    : /vendas/{id_venda}      - Obter venda por ID
- OK Update (PUT)    : /vendas/{id_venda}      - Atualizar venda por ID
- OK Delete (DELETE) : /vendas/{id_venda}      - Remover venda por ID
'''

# Definindo o Blueprint para vendas
bp_vendas = Blueprint('vendas', __name__, url_prefix='/vendas')

# >>>>>>     Listar todas as vendas (PAINEL ADMIN)
@bp_vendas.route('/', methods=['GET'])
def listar_vendas():
    stmt = db.select(Venda)
    vendas = db.session.scalars(stmt).all()
    vendas_dict = [v.to_dict() for v in vendas]
    return jsonify(vendas_dict)

# >>>>>>     Crud - Cadastrar nova venda
@bp_vendas.route('/cadastrar', methods=['POST'])
def cadastrar_venda():
    dados_requisicao = request.get_json()

    if not dados_requisicao:
        return jsonify({'Erro': 'Todos os campos devem ser preenchidos'}), 400

    # Lista de campos obrigatórios
    campos_obrigatorios = ['cliente_id', 'produto', 'quantidade', 'valor_total', 'data_venda']

    # Verifica se todos os campos obrigatórios estão presentes e não vazios
    for campo in campos_obrigatorios:
        if campo not in dados_requisicao or not dados_requisicao[campo]:
            return jsonify({'Erro': f'O campo "{campo}" é obrigatório.'}), 400

    # Verifica se o cliente existe
    cliente = db.session.execute(select(Usuario).where(Usuario.id == dados_requisicao['cliente_id'])).scalar_one_or_none()
    if not cliente:
        return jsonify({'Erro': 'Cliente não encontrado.'}), 404

    # Valida quantidade e valor_total
    try:
        quantidade = int(dados_requisicao['quantidade'])
        valor_total = float(dados_requisicao['valor_total'])
        if quantidade <= 0 or valor_total <= 0:
            raise ValueError
    except ValueError:
        return jsonify({'Erro': 'Quantidade e valor_total devem ser números positivos.'}), 400

    # Valida data
    try:
        data_venda = datetime.fromisoformat(dados_requisicao['data_venda']).date()
    except ValueError:
        return jsonify({'Erro': 'Data de venda inválida. Use formato YYYY-MM-DD.'}), 400

    # Cria uma nova instância de Venda
    nova_venda = Venda(
        cliente_id=dados_requisicao['cliente_id'],
        produto=dados_requisicao['produto'],
        quantidade=quantidade,
        valor_total=valor_total,
        data_venda=data_venda
    )

    # INSERT INTO tb_venda
    db.session.add(nova_venda)
    db.session.commit()
    return jsonify({'resposta': 'Venda cadastrada com sucesso!'}), 201

# >>>>>>    cRud - Obter venda por ID
@bp_vendas.route('/<int:id_venda>', methods=['GET'])
def obter_venda(id_venda):
    # Selecionar um registro específico
    stmt = select(Venda).where(Venda.id == id_venda)
    venda = db.session.execute(stmt).scalar_one_or_none()
    if venda:
        return jsonify(venda.to_dict()), 200
    return jsonify({'Erro': 'Venda não encontrada'}), 404

# >>>>>>    crUd - Atualizar venda por ID
@bp_vendas.route('/atualizar/<int:id_venda>', methods=['PUT'])
def atualizar_venda(id_venda):
    dados_requisicao = request.get_json()

    if not dados_requisicao:
        return jsonify({'Erro': 'Nenhum dado enviado para atualização.'}), 400

    venda_selecionada = db.session.execute(
        select(Venda).where(Venda.id == id_venda)
    ).scalar_one_or_none()

    if not venda_selecionada:
        return jsonify({'Erro': 'Venda não encontrada'}), 404

    # Lista de campos permitidos para atualização
    campos_permitidos = {'cliente_id', 'produto', 'quantidade', 'valor_total', 'data_venda'}

    for campo in campos_permitidos:
        if campo in dados_requisicao:
            if campo == 'cliente_id':
                cliente = db.session.execute(select(Usuario).where(Usuario.id == dados_requisicao['cliente_id'])).scalar_one_or_none()
                if not cliente:
                    return jsonify({'Erro': 'Cliente não encontrado.'}), 404
            elif campo == 'quantidade':
                try:
                    quantidade = int(dados_requisicao['quantidade'])
                    if quantidade <= 0:
                        raise ValueError
                    setattr(venda_selecionada, campo, quantidade)
                    continue
                except ValueError:
                    return jsonify({'Erro': 'Quantidade deve ser um número positivo.'}), 400
            elif campo == 'valor_total':
                try:
                    valor_total = float(dados_requisicao['valor_total'])
                    if valor_total <= 0:
                        raise ValueError
                    setattr(venda_selecionada, campo, valor_total)
                    continue
                except ValueError:
                    return jsonify({'Erro': 'Valor total deve ser um número positivo.'}), 400
            elif campo == 'data_venda':
                try:
                    data_venda = datetime.fromisoformat(dados_requisicao['data_venda']).date()
                    setattr(venda_selecionada, campo, data_venda)
                    continue
                except ValueError:
                    return jsonify({'Erro': 'Data de venda inválida. Use formato YYYY-MM-DD.'}), 400
            setattr(venda_selecionada, campo, dados_requisicao[campo])

    db.session.commit()
    return jsonify({'resposta': 'Venda atualizada com sucesso!'}), 200

# >>>>>>     cruD - Remover venda por ID
@bp_vendas.route('/remover/<int:id_venda>', methods=['DELETE'])
def remover_venda(id_venda):

    venda = db.session.execute(
        select(Venda).where(Venda.id == id_venda)
    ).scalar_one_or_none()

    if venda:
        db.session.delete(venda)
        db.session.commit()
        return jsonify({'resposta': 'Venda removida com sucesso!'}), 200

    return jsonify({'Erro': 'Venda não encontrada'}), 404