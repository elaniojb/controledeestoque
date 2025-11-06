from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#class Usuario(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    nome = db.Column(db.String(100), nullable=False)


#class Instituicao(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    nome = db.Column(db.String(100), nullable=False)
#    endereco = db.Column(db.String(100), nullable=True)


class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=True)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=True)


class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    fornecedor = db.relationship('Fornecedor', backref=db.backref('compras', lazy=True))
    data = db.Column(db.DateTime, nullable=False)


class CompraProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)  ## Preço do produto no momento da compra

    compra = db.relationship('Compra', backref=db.backref('compra_produtos', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('compra_produtos', lazy=True))
    