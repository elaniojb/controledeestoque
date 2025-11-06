from sqlalchemy import and_
from datetime import datetime
from app import db  # ajuste conforme a sua estrutura
from models import Compra, CompraProduto, Produto  # ajuste conforme necessário
from flask import render_template, request, flash

def compra_produtos(fornecedor, produtos, quantd, precos_unit):
    for produto_id, quantidade, preco_unitario in zip(produtos, quantd, precos_unit):

        # Verifica se já existe esse produto no estoque
        item_existente = CompraProduto.query.filter_by(produto_id=produto_id).first()

        if item_existente:
            # Se já existir, atualiza a quantidade
            item_existente.quantidade += int(quantidade)
        else:
            # Se não existir, cria nova compra e item
            nova_compra = Compra(fornecedor_id=fornecedor, data=datetime.now())
            db.session.add(nova_compra)
            db.session.commit()

            novo_item = CompraProduto(
                compra_id=nova_compra.id,
                produto_id=int(produto_id),
                quantidade=int(quantidade),
                preco_unitario=float(preco_unitario)
            )

            db.session.add(novo_item)

    db.session.commit()

def compra_existe(compra_id, produto_id):
    return db.session.query(CompraProduto).filter_by(
        compra_id=compra_id,
        produto_id=produto_id
    ).first()

