from src.model import db # Traz a instancia do SQLAlchemy para esse arquivo
from sqlalchemy.schema import Column # Importa o recurso para transformar atributos em colunas
from sqlalchemy.types import String, DECIMAL, Integer # Importa os tipos de dados para o MySQL


class Usuario(db.Model): # Classe que representa a tabela de usuários no banco de dados
    __tablename__ = 'tb_usuario' # Nome da tabela no banco de dados
    
    # OS ATRIBUTOS ABAIXO IRÃO CRIAR AS COLUNAS DA TABELA
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    sobrenome = Column(String(50), nullable=False)
    data_nascimento = Column(String(10), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    celular = Column(String(15), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default='user')

    # Método construtor para inicializar os atributos do usuário
    def __init__(self, nome, sobrenome, data_nascimento, cpf, celular, email, senha, role='user'):
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.celular = celular
        self.email = email
        self.senha = senha
        self.role = role
        
    # Método para converter o objeto em um dicionário, útil para serialização
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "data_nascimento": self.data_nascimento,
            "cpf": self.cpf,
            "celular": self.celular,
            "email": self.email,
            "role": self.role,
        }
