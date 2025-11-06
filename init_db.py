import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


#INSERÇÃO PADRÃO DE USUÁRIOS
cur.execute("INSERT INTO usuario (nome) VALUES (?)",
            ('José Ivan',)
            )

#INSERÇÃO PADRÃO DE INSTITUIÇÕES
cur.execute("INSERT INTO instituicao (nome, endereco) values (?,?)",
            ('Residencial Amor em Família', 'Rua São Benedito, 518',)
            )

#INSERÇÃO PADRÃO DE FORNECEDORES
cur.execute("INSERT INTO fornecedor (nome, endereco) values (?,?)",
            ('Supermercado A',"Avenida Primeira, 1",)
            )

#INSERÇÃO PADRÃO DE PRODUTOS
cur.execute("INSERT INTO produto (nome) values (?)",
            ('Produto ABC',)
            )

connection.commit()
connection.close()
