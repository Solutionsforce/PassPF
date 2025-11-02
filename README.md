# Sistema de Agendamento de Passaporte - Polícia Federal

Sistema de agendamento para emissão de passaportes brasileiro, desenvolvido com Flask e integração com pagamentos PIX via 4M Payments.

## 🚀 Deploy no Heroku

### Pré-requisitos
- Conta no [Heroku](https://heroku.com)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) instalado
- Git instalado

### Passo a Passo

#### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd <nome-do-projeto>
```

#### 2. Login no Heroku
```bash
heroku login
```

#### 3. Crie uma nova aplicação
```bash
heroku create nome-da-sua-app
```

#### 4. Configure as variáveis de ambiente (IMPORTANTE!)
```bash
# Chave secreta da sessão (gere uma chave aleatória segura)
heroku config:set SESSION_SECRET="sua_chave_secreta_super_segura_aqui"

# Token da API 4M Payments
heroku config:set FOURM_PAYMENTS_API_TOKEN="seu_token_4m_payments_aqui"
```

**⚠️ IMPORTANTE:** Nunca compartilhe ou commite essas chaves no Git!

#### 5. Deploy da aplicação
```bash
git add .
git commit -m "Deploy inicial"
git push heroku main
```

ou se sua branch principal é `master`:
```bash
git push heroku master
```

#### 6. Abra a aplicação
```bash
heroku open
```

#### 7. Visualizar logs (para debug)
```bash
heroku logs --tail
```

## 📋 Variáveis de Ambiente Necessárias

| Variável | Descrição | Obrigatória |
|----------|-----------|-------------|
| `SESSION_SECRET` | Chave secreta para sessões Flask | ✅ Sim |
| `FOURM_PAYMENTS_API_TOKEN` | Token de autenticação da API 4M Payments | ✅ Sim |

## 🔒 Segurança

- ✅ Todas as chaves de API estão em variáveis de ambiente
- ✅ Arquivo `.env.example` fornecido como template
- ✅ `.gitignore` configurado para proteger arquivos sensíveis
- ✅ Sem chaves expostas no código

## 🛠️ Estrutura do Projeto

```
.
├── app.py                          # Aplicação Flask principal
├── templates/                      # Templates HTML
│   ├── index.html
│   ├── nova_solicitacao.html
│   ├── dados_pessoais.html
│   ├── dados_complementares.html
│   ├── documentos.html
│   ├── protocolo.html
│   ├── checkout.html
│   └── sucesso.html
├── static/                         # Arquivos estáticos
│   ├── css/
│   └── js/
├── unidades_atendimento.json      # Dados das unidades da PF
├── Procfile                       # Configuração Heroku
├── runtime.txt                    # Versão do Python
├── requirements.txt               # Dependências Python
├── .gitignore                     # Arquivos ignorados pelo Git
├── .env.example                   # Exemplo de variáveis de ambiente
└── README.md                      # Este arquivo
```

## 🔧 Desenvolvimento Local

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Configurar variáveis de ambiente
Copie `.env.example` para `.env` e configure suas chaves:
```bash
cp .env.example .env
# Edite o arquivo .env com suas chaves reais
```

### Executar localmente
```bash
python app.py
```

Acesse: `http://localhost:5000`

## 📦 Tecnologias Utilizadas

- **Backend:** Flask 3.0.0
- **Servidor WSGI:** Gunicorn 21.2.0
- **PDF:** ReportLab 4.4.4
- **Timezone:** pytz 2025.2
- **HTTP Requests:** requests 2.32.5
- **Pagamentos:** 4M Payments API

## 🌐 Endpoints Principais

- `/` - Página inicial
- `/nova-solicitacao` - Início do processo de solicitação
- `/protocolo` - Seleção de unidade e agendamento
- `/checkout` - Pagamento PIX
- `/sucesso` - Confirmação de pagamento

## 💳 Integração de Pagamentos

O sistema utiliza a API 4M Payments para processar pagamentos PIX:
- Geração automática de QR Code
- Código PIX copia e cola
- Verificação automática de pagamento
- Redirecionamento após confirmação

## 📞 Suporte

Para problemas ou dúvidas sobre o deploy, consulte:
- [Documentação Heroku](https://devcenter.heroku.com/)
- [Documentação Flask](https://flask.palletsprojects.com/)

## ⚖️ Licença

Projeto educacional - Sistema de agendamento de passaportes Polícia Federal.
