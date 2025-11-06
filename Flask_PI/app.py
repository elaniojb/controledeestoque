from flask import Flask, render_template, request, url_for, flash, redirect
from models import db, Fornecedor, Produto, CompraProduto
from services.Produto.produto_services import *
from services.Fornecedor.fornecedor_services import *
from services.Compra.compra_produtos import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    compras = CompraProduto.query.all()
    #return render_template("index.html", compras=compras)
    return render_template("index.html",compras=compras)

@app.route('/<int:id>/delete', methods=('POST',))
def del_inventario(id):
    compra = CompraProduto.query.get(id)

    db.session.delete(compra)
    db.session.commit()

    flash('Removido com sucesso!',"success")
    return redirect(url_for('index'))

@app.route('/<int:id>/compra', methods=('GET', 'POST'))
def edit_compra(id):
    compra = CompraProduto.query.get(id)

    if not compra:
        flash("Compra não encontrada!", "danger")
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            compra.quantidade = request.form['Nova quantidade']
            if int (compra.quantidade) <= 0 :  
                flash("Quantidade deve ser maior que zero!", "danger")
                return render_template('edit_inventario.html', compra=compra)

            db.session.add(compra)
            db.session.commit()

            flash('Quantidade alterada com sucesso!','success')
            return redirect(url_for('index'))
        return render_template('edit_inventario.html', compra=compra)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/list/produto', methods=('GET', 'POST'))
def list_produto():
    if request.method == 'GET':
        produtos = Produto.query.all()
        return render_template("list_produto.html", produtos=produtos)
    else:
        nome = request.form['produto']
        if not nome:
            flash("Informe pelo menos um critério de pesquisa!", "danger")
            return redirect(url_for('list_produto'))

        produtos = filtrar_produto(nome)
        
        if not produtos:
            flash("Nenhum produto encontrado com os critérios informados.", "warning")

        return render_template("list_produto.html", produtos=produtos)


@app.route('/produto', methods=('GET', 'POST'))
def new_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        marca = request.form['marca']

        produto = Produto(nome=nome, marca=marca)

        if produto_existe(nome, marca):
            flash("Produto já cadastrado!", "danger")
            return redirect(url_for('list_produto'))

        db.session.add(produto)
        db.session.commit()
        flash("Produto adicionado com sucesso!", "success")
        return redirect(url_for('list_produto'))
        
    return render_template('new_produto.html')


@app.route('/<int:id>/produto', methods=('GET', 'POST'))
def edit_produto(id):
    produto = Produto.query.get(id)

    if not produto:
        flash("Produto não encontrado!", "danger")
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            produto.nome = request.form['nome']
            produto.marca = request.form['marca']

            db.session.add(produto)
            db.session.commit()

            flash('Produto alterado com sucesso!','success')
            return redirect(url_for('list_produto'))

    return render_template('edit_produto.html', produto=produto)


@app.route('/<int:id>/delete', methods=('POST',))
def del_produto(id):
    produto = Produto.query.get(id)

    db.session.delete(produto)
    db.session.commit()

    flash('"{}" foi removido com sucesso!'.format(produto.nome),"success")
    return redirect(url_for('list_produto'))


@app.route('/list/fornecedor', methods=('GET', 'POST'))
def list_fornecedor():
    if request.method == 'GET': 
        fornecedores = Fornecedor.query.all()       
        return render_template("list_fornecedor.html", fornecedores=fornecedores)
    else:
        nome = request.form['fornecedor']
        if not nome:
            flash("Informe pelo menos um critério de pesquisa!", "danger")
            return redirect(url_for('list_fornecedor'))

        fornecedores = filtrar_fornecedor(nome)
        
        if not fornecedores:
            flash("Nenhum produto encontrado com os critérios informados.", "warning")

        return render_template("list_fornecedor.html", fornecedores=fornecedores)


@app.route('/fornecedor', methods=('GET', 'POST'))
def new_fornecedor():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']

        fornecedor = Fornecedor(nome=nome, endereco=endereco)

        if fornecedor_existe(nome, endereco):
            flash("Fornecedor já cadastrado!", "danger")
            return redirect(url_for('list_fornecedor'))

        db.session.add(fornecedor)
        db.session.commit()
        return redirect(url_for('list_fornecedor'))

    return render_template('new_fornecedor.html')


@app.route('/<int:id>/fornecedor', methods=('GET', 'POST', 'DELETE'))
def edit_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)

    if not fornecedor:
        flash("Fornecedor não encontrado!", "danger")
        return redirect(url_for('index'))
    else:
        print(request.method)
        if request.method == 'POST':
            fornecedor.nome = request.form['nome']
            fornecedor.endereco = request.form['endereco']

            db.session.add(fornecedor)
            db.session.commit()

            flash('Fornecedor alterado com sucesso!','success')
            return redirect(url_for('list_fornecedor'))

    return render_template('edit_fornecedor.html', fornecedor=fornecedor)


@app.route('/<int:id>/fornecedor/delete', methods=('POST',))
def del_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)

    db.session.delete(fornecedor)
    db.session.commit()

    flash('"{}" foi removido com sucesso!'.format(fornecedor.nome), "success")
    return redirect(url_for('list_fornecedor'))


@app.route('/compra', methods=['GET','POST'])
def cadastro_compra():
    fornecedores = Fornecedor.query.all()
    produtos = Produto.query.all()
    
    if request.method == 'POST':
        fornecedor_id = request.form['fornecedor']
        produtos_ids = request.form.getlist('produto_id')
        quantidades = request.form.getlist('quantidade')
        precos_unitarios = request.form.getlist('preco_unitario')

        for quantidade, preco_unitario in zip(quantidades, precos_unitarios):
            if int(quantidade) <= 0 or float(preco_unitario) <= 0:
                flash("Quantidade e preço unitário devem ser maiores que zero!", "danger")
                return render_template('cadastro_compra.html', fornecedores=fornecedores, produtos=produtos)

        compra_produtos(fornecedor_id, produtos_ids, quantidades, precos_unitarios)
        
        return redirect(url_for('index'))

    return render_template('cadastro_compra.html', fornecedores=fornecedores, produtos=produtos)


if __name__ == '__main__':
    app.run(debug=True)