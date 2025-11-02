from flask import Flask, render_template, request, redirect, url_for, session, send_file, make_response
from datetime import datetime, timedelta
import random
import string
import os
import json
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'sua_chave_secreta_aqui_123456')

def carregar_unidades():
    with open('unidades_atendimento.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def encontrar_unidades_proximas(cep_usuario, limite=3):
    if not cep_usuario:
        return []
    
    cep_usuario_numerico = ''.join(filter(str.isdigit, cep_usuario))
    if len(cep_usuario_numerico) < 5:
        return []
    
    prefixo_usuario = int(cep_usuario_numerico[:5])
    
    unidades = carregar_unidades()
    
    unidades_com_distancia = []
    for unidade in unidades:
        cep_unidade = ''.join(filter(str.isdigit, unidade['cep']))
        if len(cep_unidade) >= 5:
            prefixo_unidade = int(cep_unidade[:5])
            distancia = abs(prefixo_usuario - prefixo_unidade)
            unidades_com_distancia.append({
                **unidade,
                'distancia': distancia
            })
    
    unidades_com_distancia.sort(key=lambda x: x['distancia'])
    
    return unidades_com_distancia[:limite]

def gerar_protocolo():
    ano = datetime.now().year
    numero_sequencial = ''.join(random.choices(string.digits, k=10))
    return f"1.{ano}.{numero_sequencial}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nova-solicitacao')
def nova_solicitacao():
    session.clear()
    return render_template('nova_solicitacao.html', secao='dados-pessoais', dados={})

@app.route('/nova-solicitacao/dados-pessoais', methods=['GET', 'POST'])
def dados_pessoais():
    if request.method == 'POST':
        session['dados_pessoais'] = request.form.to_dict()
        return redirect(url_for('documentos'))
    
    dados = session.get('dados_pessoais', {})
    return render_template('nova_solicitacao.html', secao='dados-pessoais', dados=dados)

@app.route('/nova-solicitacao/documentos', methods=['GET', 'POST'])
def documentos():
    if request.method == 'POST':
        session['documentos'] = request.form.to_dict()
        return redirect(url_for('dados_complementares'))
    
    dados = session.get('documentos', {})
    return render_template('documentos.html', secao='documentos', dados=dados)

@app.route('/nova-solicitacao/dados-complementares', methods=['GET', 'POST'])
def dados_complementares():
    if request.method == 'POST':
        session['dados_complementares'] = request.form.to_dict()
        return redirect(url_for('revisar_dados'))
    
    dados = session.get('dados_complementares', {})
    return render_template('dados_complementares.html', secao='dados-complementares', dados=dados)

@app.route('/nova-solicitacao/revisar-dados', methods=['GET', 'POST'])
def revisar_dados():
    if request.method == 'POST':
        if request.form.get('declaracao') == 'on':
            protocolo = gerar_protocolo()
            data_emissao = datetime.now().strftime('%d/%m/%Y %H:%M')
            session['protocolo'] = protocolo
            session['data_emissao'] = data_emissao
            return redirect(url_for('protocolo'))
        else:
            return redirect(url_for('revisar_dados'))
    
    dados_pessoais = session.get('dados_pessoais', {})
    dados_documentos = session.get('documentos', {})
    dados_complementares = session.get('dados_complementares', {})
    
    return render_template('revisar_dados.html', 
                         dados_pessoais=dados_pessoais,
                         dados_documentos=dados_documentos,
                         dados_complementares=dados_complementares)

@app.route('/protocolo', methods=['GET', 'POST'])
def protocolo():
    if request.method == 'POST':
        unidade_id = request.form.get('unidade_id')
        data_agendamento = request.form.get('data_agendamento')
        horario_agendamento = request.form.get('horario_agendamento')
        
        session['unidade_id'] = unidade_id
        session['data_agendamento'] = data_agendamento
        session['horario_agendamento'] = horario_agendamento
        
        return redirect(url_for('confirmacao_agendamento'))
    
    protocolo = session.get('protocolo', 'N/A')
    data_emissao = session.get('data_emissao', 'N/A')
    dados_pessoais = session.get('dados_pessoais', {})
    dados_complementares = session.get('dados_complementares', {})
    
    cep_usuario = dados_complementares.get('cep', '')
    unidades_proximas = encontrar_unidades_proximas(cep_usuario, 3)
    
    datas_disponiveis = []
    data_inicial = datetime.now() + timedelta(days=1)
    for i in range(15):
        data = data_inicial + timedelta(days=i)
        if data.weekday() < 5:
            datas_disponiveis.append(data.strftime('%Y-%m-%d'))
    
    horarios_disponiveis = [
        '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
        '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
    ]
    
    return render_template('protocolo.html',
                         protocolo=protocolo,
                         data_emissao=data_emissao,
                         dados_pessoais=dados_pessoais,
                         dados_complementares=dados_complementares,
                         unidades=unidades_proximas,
                         datas=datas_disponiveis,
                         horarios=horarios_disponiveis)

@app.route('/confirmacao')
def confirmacao():
    protocolo = session.get('protocolo', 'N/A')
    return render_template('confirmacao.html', protocolo=protocolo)

@app.route('/confirmacao-agendamento')
def confirmacao_agendamento():
    protocolo = session.get('protocolo', 'N/A')
    unidade_id = session.get('unidade_id')
    data_agendamento = session.get('data_agendamento')
    horario_agendamento = session.get('horario_agendamento')
    
    unidade_selecionada = None
    if unidade_id:
        unidades = carregar_unidades()
        for unidade in unidades:
            if str(unidade['id']) == str(unidade_id):
                unidade_selecionada = unidade
                break
    
    return render_template('confirmacao_agendamento.html',
                         protocolo=protocolo,
                         unidade=unidade_selecionada,
                         data=data_agendamento,
                         horario=horario_agendamento)

@app.route('/agendar', methods=['POST'])
def agendar():
    quantidade = request.form.get('quantidade', '1')
    
    try:
        quantidade_int = int(quantidade)
        if quantidade_int < 1 or quantidade_int > 5:
            return redirect(url_for('index'))
    except ValueError:
        return redirect(url_for('index'))
    
    protocolo = gerar_protocolo()
    data_atual = datetime.now().strftime('%d/%m/%Y às %H:%M')
    
    return render_template('confirmacao.html', 
                         quantidade=quantidade,
                         protocolo=protocolo,
                         data=data_atual)

@app.route('/download-protocolo')
def download_protocolo():
    protocolo = session.get('protocolo', 'N/A')
    data_emissao = session.get('data_emissao', 'N/A')
    dados_pessoais = session.get('dados_pessoais', {})
    dados_complementares = session.get('dados_complementares', {})
    
    buffer = BytesIO()
    
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    y = height - 50
    
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2, y, "PROTOCOLO DE SOLICITAÇÃO")
    y -= 20
    pdf.drawCentredString(width / 2, y, "DE DOCUMENTO DE VIAGEM")
    y -= 40
    
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1.5)
    pdf.rect(50, y - 200, width - 100, 200, stroke=1, fill=0)
    
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(70, y - 25, "Tipo de Documento de Viagem:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(280, y - 25, "PASSAPORTE COMUM - ICAO")
    
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(70, y - 45, "Emissão do Protocolo:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(280, y - 45, data_emissao)
    
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(70, y - 75, f"Protocolo: {protocolo}")
    
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(70, y - 105, "Dados da Solicitação")
    
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(70, y - 125, "Requerente:")
    
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(70, y - 145, "Nome Completo:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(170, y - 145, dados_pessoais.get('nome', '').upper())
    
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(70, y - 160, "Sexo:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(170, y - 160, dados_pessoais.get('sexo', '').capitalize())
    
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(280, y - 160, "Data de Nascimento:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(400, y - 160, dados_pessoais.get('data_nascimento', ''))
    
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(70, y - 180, "Endereço:")
    pdf.setFont("Helvetica", 8)
    endereco_completo = f"{dados_complementares.get('logradouro', '').upper()} - {dados_complementares.get('bairro', '').upper()}"
    pdf.drawString(170, y - 180, endereco_completo)
    
    cidade_uf = f"{dados_complementares.get('cidade_endereco', '').upper()}/{dados_complementares.get('uf_endereco', '').upper()} - BRASIL"
    pdf.drawString(170, y - 193, cidade_uf)
    
    y -= 220
    
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "INFORMAÇÕES IMPORTANTES:")
    y -= 20
    
    informacoes = [
        "- Caso o documento de viagem não seja retirado no prazo de 90 (noventa) dias, contados a",
        "  partir da confirmação de pedido de passaporte no posto da PF, o mesmo será cancelado;",
        "",
        "- A solicitação de passaporte preenchida eletronicamente e não confirmada, no posto da PF,",
        "  em até 90 (noventa) dias será cancelada automaticamente;",
        "",
        "- Os documentos apresentados poderão ser recusados se o tempo de expedição e/ou o mau",
        "  estado de conservação impossibilitarem a identificação do requerente;",
        "",
        "- O simples agendamento e/ou recibo bancário não comprova o pagamento da taxa;",
        "",
        "- Para crianças menores de 3 anos de idade deverá ser apresentada 1(uma) fotografia facial,",
        "  tamanho 5X7, recente, colorida, sem data e em fundo branco.",
        "",
        "- Em algumas unidades é obrigatório o agendamento prévio do atendimento pelo site",
        "  www.dpf.gov.br.",
        "",
        "- Comparecer ao Posto de Atendimento do Departamento de Polícia Federal, munido deste",
        "  protocolo e de documentos originais, para validação e coleta de foto, impressões digitais",
        "  e assinatura."
    ]
    
    pdf.setFont("Helvetica", 9)
    for info in informacoes:
        pdf.drawString(50, y, info)
        y -= 12
    
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawString(50, 30, f"Documento gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    
    pdf.save()
    
    buffer.seek(0)
    
    response = make_response(send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'protocolo_{protocolo.replace(".", "-")}.pdf'
    ))
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
