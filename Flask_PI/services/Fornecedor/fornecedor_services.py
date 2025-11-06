from models import Fornecedor
from sqlalchemy import and_ 


def fornecedor_existe(nome, endereco):
    return Fornecedor.query.filter(
        and_(Fornecedor.nome == nome, Fornecedor.endereco == endereco)
    ).first() is not None

def filtrar_fornecedor(nome):
    return Fornecedor.query.filter(
        Fornecedor.nome.like(f"%{nome}%")
    ).all()
