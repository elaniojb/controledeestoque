import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_produto(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produto WHERE id = ?',
                           (id,)).fetchone()
    conn.close()
    if produto is None:
        abort(404)
    return produto


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/list/produto', methods=('GET',))
def list_produto():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produto').fetchall()
    conn.close()
    return render_template("list_produto.html", produtos=produtos)


@app.route('/produto', methods=('GET', 'POST'))
def new_produto():
    if request.method == 'POST':
        nome = request.form['nome']

        if not nome:
            flash('É necessário informar o nome do produto!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO produto (nome) VALUES (?)',
                         (nome,))
            conn.commit()
            conn.close()
            return redirect(url_for('list_produto'))

    return render_template('new_produto.html')


@app.route('/<int:id>/produto', methods=('GET', 'POST'))
def edit_produto(id):
    produto = get_produto(id)

    if request.method == 'POST':
        nome = request.form['nome']

        if not nome:
            flash('É necessário informar o nome do produto!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE produto SET nome = ?'
                         ' WHERE id = ?',
                         (nome, id)
                         )
            conn.commit()
            conn.close()
            flash('Produto alterado com sucesso!')
            return redirect(url_for('list_produto'))

    return render_template('edit_produto.html', produto=produto)


@app.route('/<int:id>/delete', methods=('POST',))
def del_produto(id):
    produto = get_produto(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM produto WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi removido com sucesso!'.format(produto['nome']))
    return redirect(url_for('list_produto'))
