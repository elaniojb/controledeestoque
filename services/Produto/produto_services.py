from models import Produto
from sqlalchemy import and_ 


def produto_existe(nome, marca):
    return Produto.query.filter(
        and_(Produto.nome == nome, Produto.marca == marca)
    ).first() is not None

def filtrar_produto(nome): 
    return Produto.query.filter(
        Produto.nome.like(f"%{nome}%")
    ).all()