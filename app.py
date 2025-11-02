from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import random
import string

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui_123456'

def gerar_protocolo():
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    numeros = ''.join(random.choices(string.digits, k=8))
    return f"{letras}-{numeros[:4]}-{numeros[4:]}"

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
        return redirect(url_for('confirmacao'))
    
    dados_pessoais = session.get('dados_pessoais', {})
    dados_documentos = session.get('documentos', {})
    dados_complementares = session.get('dados_complementares', {})
    
    return render_template('revisar_dados.html', 
                         dados_pessoais=dados_pessoais,
                         dados_documentos=dados_documentos,
                         dados_complementares=dados_complementares)

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
