DROP TABLE IF EXISTS usuario;

CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome varchar(100) not null
);

DROP TABLE IF EXISTS instituicao;

CREATE TABLE instituicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome varchar(100) not null,
    endereco varchar(100) null
);

DROP TABLE IF EXISTS fornecedor;

CREATE TABLE fornecedor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome varchar(100) not null,
    endereco varchar(100) null
);

DROP TABLE IF EXISTS produto;

CREATE TABLE produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome varchar(100) not null,
    preco decimal(10,2) null,
    quantidade integer null,
    marca varchar(100) null,
);
