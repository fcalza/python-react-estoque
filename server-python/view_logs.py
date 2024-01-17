from flask import jsonify
from flask_marshmallow import Marshmallow
from sqlalchemy import asc, func

from app import app
from models import LogProduto, db

ma=Marshmallow(app)


class LogProdutoSchema(ma.Schema):
    class Meta:
        fields = ('id','produto_id','nome_produto','quantidade','local',
                  'tipo_operacao', 'data_hora', 'created_at')


log_produtos_schema = LogProdutoSchema(many=True)


@app.route('/log_produto/entradas', methods=['GET'])
def log_entrada_produtos():
    logs = LogProduto.query.filter_by(tipo_operacao='entrada').all()
    results = log_produtos_schema.dump(logs)
    return jsonify(results)  


@app.route('/log_produto/saidas', methods=['GET'])
def log_saida_produtos():
    logs = LogProduto.query.filter_by(tipo_operacao='saida').all()
    results = log_produtos_schema.dump(logs)
    return jsonify(results)


@app.route('/grafico/entradas', methods=['GET'])
def log_graficos_entradas():
    logs = (
        db.session.query(
            func.date_format(LogProduto.data_hora, '%m/%Y').label('mes_ano'),
            func.sum(LogProduto.quantidade).label('total_quantidade')
        )
        .filter(LogProduto.tipo_operacao == 'entrada')
        .group_by('mes_ano')
        .order_by(asc(func.max(LogProduto.data_hora)))
        .all()
    )
    logs_dict = [{'mes_ano': row.mes_ano, 'total_quantidade': float(row.total_quantidade)} for row in logs]
    
    return jsonify(logs_dict)


@app.route('/grafico/saidas', methods=['GET'])
def log_graficos_saidas():
    logs = (
        db.session.query(
            func.date_format(LogProduto.data_hora, '%m/%Y').label('mes_ano'),
            func.sum(LogProduto.quantidade).label('total_quantidade')
        )
        .filter(LogProduto.tipo_operacao == 'saida')
        .group_by('mes_ano')
        .order_by(asc(func.max(LogProduto.data_hora)))
        .all()
    )
    logs_dict = [{'mes_ano': row.mes_ano, 'total_quantidade': float(row.total_quantidade)} for row in logs]
    
    return jsonify(logs_dict)
