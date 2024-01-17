from io import BytesIO
from flask import jsonify, request, send_file
from reportlab.pdfgen import canvas
from flask_marshmallow import Marshmallow
from sqlalchemy import exc

from app import app
from models import LogProduto, db, Produto
from helper import converter_data, gerar_pdf_logs, registrar_log


db.init_app(app)

with app.app_context():
    db.create_all()

ma=Marshmallow(app)


class ProdutoSchema(ma.Schema):
    class Meta:
        fields = ('id','nome','numero_registro','fabricante','tipo','descricao', 'quantidade')

produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True)


class LogProdutoSchema(ma.Schema):
    class Meta:
        fields = ('id','produto_id','nome_produto','quantidade','local','tipo_operacao','created_at')

log_produtos_schema = LogProdutoSchema(many=True)


@app.route("/")
def rotas():
    array = []
    for rule in app.url_map.iter_rules():
        array.append({
            "methods": list(rule.methods),
            "route": str(rule)
        })
    return jsonify(array)


@app.route('/produtos', methods=['GET']) 
def produtos():
    produtos = Produto.query.all()
    results = produtos_schema.dump(produtos)
    return jsonify(results)


@app.route('/produto/<id>',methods =['GET'])
def produto(id):
    produto = Produto.query.get(id)
    return produto_schema.jsonify(produto)


@app.route('/produto/add', methods=['PUT'])
def newuser():
    try:
        if request.json['numero_registro']:
            registro = request.json['numero_registro']
            if Produto.query.filter_by(numero_registro=registro).first():
                return jsonify({'error': 'Numero de registro já cadastrado.'}), 400
        else:
            return jsonify({'error': 'Necessário informar número registro.'}), 400

        produto = Produto(
            nome=request.json['nome'], 
            numero_registro=registro,
            fabricante=request.json.get('fabricante'),
            tipo=request.json.get('tipo'),
            descricao=request.json.get('descricao'),
        )

        db.session.add(produto)
        db.session.commit()
        registrar_log(produto.id, produto.nome, 0, 'adicionar')

        return produto_schema.jsonify(produto), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': f'Não foi possível atualizar o produto. Número de registro duplicado', 'Detalhes': {str(e)}}), 400
    except KeyError:
        return jsonify({'error': 'É necessário informar ao minimo os campos de "nome" e "numero_registro"'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Não foi possível adicionar o produto.', 'Detalhes': {str(e)}}), 400 


@app.route('/produto/atualizar/<id>',methods = ['PUT'])
def produto_atualizar(id):
    try:
        produto = Produto.query.get(id)
        if not produto:
            return jsonify({'error': 'Produto não encontrado.'}), 400
        
        if request.json['numero_registro']:
            registro = request.json['numero_registro']
            valida_registro_ja_cadastrado = Produto.query.filter_by(numero_registro=registro).first()
            if valida_registro_ja_cadastrado and valida_registro_ja_cadastrado.id != produto.id:
                return jsonify({'error': 'Número de registro já cadastrado.'}), 400
        else:
            return jsonify({'error': 'Necessário informar número registro.'}), 400

        produto.nome=request.json['nome']
        produto.numero_registro=registro
        produto.fabricante=request.json.get('fabricante')
        produto.tipo=request.json.get('tipo')
        produto.descricao=request.json.get('descricao')

        db.session.commit()
        
        return produto_schema.jsonify(produto)
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': f'Não foi possível atualizar o produto. Número de registro duplicado', 'Detalhes': {str(e)}}), 400
    except KeyError:
        return jsonify({'error': 'É necessário informar ao minimo os campos de "nome" e "numero_registro"'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Não foi possível adicionar o produto.', 'Detalhes': {str(e)}}), 400


@app.route('/produto/delete/<id>',methods=['DELETE'])
def produto_del(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    registrar_log(produto.id, produto.nome, 0, 'remover')
    return produto_schema.jsonify(produto)


#/produto/gerencia?tipo=entrada&dataInicio=${dataInicio}&dataFim=${dataFim}`
@app.route('/produto/gerencia', methods=['GET'])
def produto_gerencia():
    tipo = request.args.get('tipo')
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')
    if not tipo or not data_inicio or not data_fim:
        return jsonify({'error': 'Verifique os campos informados'}), 400
    data_inicio = converter_data(data_inicio)
    data_fim = converter_data(data_fim)
    if data_inicio > data_fim:
        return jsonify({'error': 'Data inicio deve ser menor que data fim'}), 400
    if (data_fim - data_inicio).days > 31:
        return jsonify({'error': 'Intervalo de datas deve ser menor que 31 dias'}), 400

    data_inicio = data_inicio.replace(hour=0, minute=0, second=0)
    data_fim = data_fim.replace(hour=23, minute=59, second=59)
    buffer = gerar_pdf_logs(data_inicio, data_fim)

    if not buffer:
        print(4)
        return jsonify({'error': 'Nenhum registro encontrado'}), 400

    nome = 'entradas.pdf' if tipo == 'entrada' else 'saidas.pdf'
    return send_file(buffer, as_attachment=True, download_name=nome)
