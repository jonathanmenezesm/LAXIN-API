from src.model import db # Traz a instancia do SQLAlchemy para esse arquivo
from sqlalchemy.schema import Column, ForeignKey # Importa o recurso para transformar atributos em colunas
from sqlalchemy.types import String, DECIMAL, Integer, Date # Importa os tipos de dados para o MySQL
from sqlalchemy.orm import relationship


class Venda(db.Model): # Classe que representa a tabela de vendas no banco de dados
    __tablename__ = 'tb_venda' # Nome da tabela no banco de dados

    # OS ATRIBUTOS ABAIXO IRÃO CRIAR AS COLUNAS DA TABELA
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('tb_usuario.id'), nullable=False)
    produto = Column(String(100), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_total = Column(DECIMAL(10, 2), nullable=False)
    data_venda = Column(Date, nullable=False)

    # Relacionamento com Usuario
    cliente = relationship('Usuario', backref='vendas')

    # Método construtor para inicializar os atributos da venda
    def __init__(self, cliente_id, produto, quantidade, valor_total, data_venda):
        self.cliente_id = cliente_id
        self.produto = produto
        self.quantidade = quantidade
        self.valor_total = valor_total
        self.data_venda = data_venda

    # Método para converter o objeto em um dicionário, útil para serialização
    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "produto": self.produto,
            "quantidade": self.quantidade,
            "valor_total": str(self.valor_total),  # DECIMAL para string
            "data_venda": self.data_venda.isoformat() if self.data_venda else None,
            "cliente_nome": self.cliente.nome + ' ' + self.cliente.sobrenome if self.cliente else None,
        }