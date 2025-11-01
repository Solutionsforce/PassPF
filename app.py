from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import random
import string

app = Flask(__name__)

def gerar_protocolo():
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    numeros = ''.join(random.choices(string.digits, k=8))
    return f"{letras}-{numeros[:4]}-{numeros[4:]}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nova-solicitacao')
def nova_solicitacao():
    return render_template('nova_solicitacao.html')

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
