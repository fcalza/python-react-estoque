
import pytz
import time

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

from models import LogProduto, db


def registrar_log(produto_id: int, nome_produto: str, quantidade: int, tipo_operacao: str, 
                  local: str = None, data_hora=datetime.now()) -> None:
    log = LogProduto(
        produto_id=produto_id,
        nome_produto=nome_produto,
        quantidade=quantidade,
        tipo_operacao=tipo_operacao,
        local=local,
        data_hora=data_hora
    )
    db.session.add(log)
    db.session.commit()


def converter_data(data_hora: str) -> datetime:
    """
    Converte a string de data e hora para o formato datetime
    data_hora: str - data e hora no formato ISO 8601 2024-01-16T03:00:00.000Z
    """    
    data_hora_dt = datetime.strptime(data_hora, "%Y-%m-%dT%H:%M:%S.%fZ")
    fuso_horario = pytz.timezone('America/Sao_Paulo') # @TODO: pegar do config sistema
    data_hora_dt = data_hora_dt.replace(tzinfo=pytz.utc).astimezone(fuso_horario)
    return data_hora_dt


def gerar_pdf_logs(data_inicio: datetime, data_fim: datetime) -> [BytesIO, None]:
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    data = db.session.query(
        LogProduto.nome_produto.label('Nome Produto'),
        LogProduto.quantidade.label('Quantidade'),
        LogProduto.local.label('Local'),
        LogProduto.tipo_operacao.label('Tipo Operação'),
        LogProduto.created_at.label('Data').cast(db.String).label('Data Formatada')
    ).filter(LogProduto.tipo_operacao.in_(['entrada', 'saida']),
             LogProduto.data_hora.between(data_inicio, data_fim)
    ).all()
    
    if not data:
        return None
    
    table = Table([
        ['Nome Produto', 'Quantidade', 'Local', 'Tipo Operação', 'Data'],
        *[list(row) for row in data]
    ])
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#77B5FE'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1, 1)),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), '#D5E4F3')])
    table.setStyle(style)
    styles = getSampleStyleSheet()
    title = Paragraph('<b>Registros de Entrada e Saída</b>', styles['Title'])
    elements = [title, table]
    pdf.build(elements)
    buffer.seek(0)
    return buffer
