from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import random
import string
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'sua_chave_secreta_aqui_123456')

def carregar_unidades():
    with open('unidades_pf.json', 'r', encoding='utf-8') as f:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
