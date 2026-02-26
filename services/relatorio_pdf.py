from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from datetime import datetime
import os

from database.execucoes import gerar_resumo_execucao
from database.conciliacoes import buscar_conciliacoes_por_execucao


def gerar_relatorio_pdf(execucao_id: int):

    # Criar pasta se não existir
    pasta_relatorios = "dados/relatorios"
    os.makedirs(pasta_relatorios, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"relatorio_execucao_{execucao_id}_{timestamp}.pdf"
    caminho_arquivo = os.path.join(pasta_relatorios, nome_arquivo)

    doc = SimpleDocTemplate(caminho_arquivo, pagesize=A4)
    elementos = []

    styles = getSampleStyleSheet()
    estilo_titulo = styles["Heading1"]
    estilo_normal = styles["Normal"]

    # Título
    elementos.append(Paragraph("RELATÓRIO DE CONCILIAÇÃO BANCÁRIA", estilo_titulo))
    elementos.append(Spacer(1, 0.5 * inch))

    # Resumo
    resumo = gerar_resumo_execucao(execucao_id)

    elementos.append(Paragraph(f"Execução ID: {execucao_id}", estilo_normal))
    elementos.append(Paragraph(f"Total AUTO: {resumo['auto']}", estilo_normal))
    elementos.append(Paragraph(f"Total SUGESTÕES: {resumo['sugestoes']}", estilo_normal))
    elementos.append(Spacer(1, 0.5 * inch))

    # Buscar conciliacoes
    conciliacoes = buscar_conciliacoes_por_execucao(execucao_id)

    dados_tabela = [["Extrato", "Controle", "Status", "Similaridade"]]

    for c in conciliacoes:
        dados_tabela.append([
            str(c["lancamento_banco_id"]),
            str(c["lancamento_controle_id"]),
            c["status"],
            f"{c['similaridade']:.2f}%"
        ])

    tabela = Table(dados_tabela)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elementos.append(tabela)

    doc.build(elementos)

    print(f"Relatório gerado em: {caminho_arquivo}")