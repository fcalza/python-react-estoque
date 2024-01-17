from flask import jsonify, request
from flask_marshmallow import Marshmallow

from app import app
from models import db, Produto
from helper import converter_data, registrar_log


ma=Marshmallow(app)


class ProdutoSchema(ma.Schema):
    class Meta:
        fields = ('id','nome','numero_registro','fabricante','tipo','descricao', 'quantidade')

produto_schema = ProdutoSchema()


@app.route('/produto/saida/<id>', methods=['POST'])
def produto_saida(id):
    if not request.is_json:
        return jsonify({'error': 'Dados JSON ausentes na requisição'}), 400
    data = request.json
    if 'quantidade' not in data or not data['quantidade']:
        return jsonify({'error': 'Verifique os campos informados'}), 400
    
    quantidade_str = data['quantidade']
    if not quantidade_str.isdigit():
        return jsonify({'error': 'Quantidade deve ser um número inteiro positivo'}), 400
    quantidade = int(quantidade_str)
    if quantidade <= 0:
        return jsonify({'error': 'Quantidade deve ser maior que zero'}), 400

    produto = Produto.query.get(id)
    if produto.quantidade < quantidade:
        return jsonify({'error': f'Quantidade maior que a disponível. Disponível: {produto.quantidade}'}), 400
    produto.quantidade -= quantidade
    
    db.session.commit()
    registrar_log(produto.id, produto.nome, quantidade, 'saida', data.get('local'),
                  converter_data(data.get('dataHora')))

    return produto_schema.jsonify(produto)


@app.route('/produto/entrada/<id>', methods=['POST'])
def produto_entrada(id):
    if not request.is_json:
        return jsonify({'error': 'Dados JSON ausentes na requisição'}), 400
    data = request.json
    if 'quantidade' not in data or not data['quantidade']:
        return jsonify({'error': 'Verifique os campos informados'}), 400
    
    quantidade_str = data['quantidade']
    if not quantidade_str.isdigit():
        return jsonify({'error': 'Quantidade deve ser um número inteiro positivo'}), 400
    quantidade = int(quantidade_str)
    if quantidade <= 0:
        return jsonify({'error': 'Quantidade deve ser maior que zero'}), 400

    produto = Produto.query.get(id)
    produto.quantidade += quantidade
    
    db.session.commit()
    registrar_log(produto.id, produto.nome, quantidade, 'entrada', data.get('local'), 
                  converter_data(data.get('dataHora')))
    return produto_schema.jsonify(produto)
