import mysql.connector
import time

try:
    conn = mysql.connector.connect(user='root', password='root', host='127.0.0.1')
except mysql.connector.Error as err:
    print(err)
    exit()

conn.cursor().execute(
    'DROP DATABASE IF EXISTS estoque;'
)
time.sleep(1)
criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `estoque`;
    USE `estoque`;
    CREATE TABLE produto (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        numero_registro VARCHAR(255) NOT NULL UNIQUE,
        fabricante VARCHAR(100),
        tipo VARCHAR(50),
        descricao TEXT,
        quantidade INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE log_produto (
        id INT AUTO_INCREMENT PRIMARY KEY,
        produto_id INT,
        nome_produto VARCHAR(255),
        quantidade INT,
        local VARCHAR(255),
        tipo_operacao ENUM('entrada', 'saida', 'remover', 'adicionar'),
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_produto_id (produto_id),
        INDEX idx_tipo_operacao (tipo_operacao)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    '''
conn.cursor().execute(criar_tabelas)
