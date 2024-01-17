from flask_sqlalchemy import SQLAlchemy
         
db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    numero_registro = db.Column(db.String(255), nullable=False, unique=True)
    fabricante = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    descricao = db.Column(db.Text)
    quantidade = db.Column(db.Integer, nullable=False, default=0)


class LogProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    nome_produto = db.Column(db.String(255))
    quantidade = db.Column(db.Integer)
    local = db.Column(db.String(255)) #local de onde recebeu entrada ou saida deveria ser uma tabela e aqui pegar o id
    tipo_operacao = db.Column(db.Enum('entrada', 'saida', 'remover', 'adicionar'))
    data_hora = db.Column(db.TIMESTAMP, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    
