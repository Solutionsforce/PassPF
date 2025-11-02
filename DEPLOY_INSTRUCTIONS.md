# 🚀 Instruções de Deploy no Heroku

## ✅ Checklist Pré-Deploy

Antes de fazer o deploy, certifique-se de que:

- [x] Procfile criado
- [x] runtime.txt com versão do Python
- [x] requirements.txt atualizado com gunicorn
- [x] .gitignore configurado
- [x] Variáveis de ambiente documentadas em .env.example
- [x] Código não contém chaves expostas

## 📝 Passo a Passo Completo

### 1️⃣ Preparar o Repositório Git

```bash
# Inicializar Git (se ainda não estiver)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Preparar aplicação para deploy no Heroku"
```

### 2️⃣ Instalar Heroku CLI

**Windows:**
Baixe e instale: https://devcenter.heroku.com/articles/heroku-cli

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### 3️⃣ Login no Heroku

```bash
heroku login
```

Isso abrirá seu navegador para fazer login.

### 4️⃣ Criar a Aplicação no Heroku

```bash
# Substituir 'meu-passaporte-pf' pelo nome desejado
heroku create meu-passaporte-pf
```

**Nota:** O nome deve ser único no Heroku. Se já existir, escolha outro nome.

### 5️⃣ Configurar Variáveis de Ambiente (CRÍTICO! 🔒)

```bash
# Gerar uma chave secreta segura para SESSION_SECRET
# Use este comando para gerar uma chave aleatória:
python -c "import secrets; print(secrets.token_hex(32))"

# Configurar SESSION_SECRET (cole a chave gerada acima)
heroku config:set SESSION_SECRET="cole_a_chave_gerada_aqui"

# Configurar token da API 4M Payments
heroku config:set FOURM_PAYMENTS_API_TOKEN="seu_token_4m_payments_aqui"
```

**⚠️ MUITO IMPORTANTE:**
- Nunca compartilhe essas chaves
- Nunca commite no Git
- Use chaves diferentes em desenvolvimento e produção

### 6️⃣ Verificar Variáveis Configuradas

```bash
heroku config
```

Você deve ver:
```
=== meu-passaporte-pf Config Vars
FOURM_PAYMENTS_API_TOKEN: xxxxxxxxxxxxxx
SESSION_SECRET:           xxxxxxxxxxxxxx
```

### 7️⃣ Deploy da Aplicação

```bash
# Se sua branch principal é 'main':
git push heroku main

# Se sua branch principal é 'master':
git push heroku master
```

### 8️⃣ Verificar Status

```bash
# Ver logs em tempo real
heroku logs --tail

# Verificar status da aplicação
heroku ps

# Abrir a aplicação no navegador
heroku open
```

## 🔍 Troubleshooting

### Erro: "Application error"

```bash
# Ver logs detalhados
heroku logs --tail
```

### Erro: "No web processes running"

```bash
# Escalar o dyno web
heroku ps:scale web=1
```

### Erro: "Module not found"

Verifique se todas as dependências estão no `requirements.txt`:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Atualizar requirements.txt"
git push heroku main
```

### Erro: "Push rejected, no Cedar-supported app detected"

Certifique-se de que:
- O arquivo `Procfile` existe (sem extensão .txt)
- O arquivo `requirements.txt` existe

### Variáveis de ambiente não estão funcionando

```bash
# Listar todas as variáveis
heroku config

# Adicionar novamente se necessário
heroku config:set NOME_VARIAVEL=valor
```

## 🔄 Atualizações Futuras

Sempre que fizer mudanças no código:

```bash
# 1. Commit das alterações
git add .
git commit -m "Descrição das mudanças"

# 2. Push para o Heroku
git push heroku main

# 3. Verificar logs
heroku logs --tail
```

## 📊 Monitoramento

### Ver logs
```bash
heroku logs --tail
```

### Reiniciar aplicação
```bash
heroku restart
```

### Verificar uso de recursos
```bash
heroku ps
```

### Abrir dashboard do Heroku
```bash
heroku open --app meu-passaporte-pf
```

## 💰 Planos do Heroku

- **Free/Eco Dyno:** Ótimo para testes (pode dormir após 30 min de inatividade)
- **Basic Dyno:** $7/mês - Não dorme, melhor para produção
- **Standard/Performance:** Para alta performance

## 🌐 Domínio Personalizado (Opcional)

```bash
# Adicionar domínio customizado
heroku domains:add www.meudominio.com.br

# Ver informações de DNS
heroku domains
```

## 🔐 Segurança Extra

### Forçar HTTPS (Recomendado para produção)

Adicione no início do `app.py`:

```python
from flask import Flask, request, redirect

@app.before_request
def before_request():
    if not request.is_secure and request.headers.get('X-Forwarded-Proto', 'http') != 'https':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```

## 📞 Comandos Úteis

```bash
# Ver todas as apps
heroku apps

# Deletar uma app
heroku apps:destroy --app nome-da-app

# Acessar console Python
heroku run python

# Executar comando personalizado
heroku run comando-aqui

# Ver addons instalados
heroku addons
```

## ✅ Checklist Pós-Deploy

- [ ] Aplicação abre sem erros (`heroku open`)
- [ ] Logs não mostram erros críticos (`heroku logs --tail`)
- [ ] Todas as páginas carregam corretamente
- [ ] Formulários funcionam
- [ ] Pagamento PIX gera QR Code
- [ ] Variáveis de ambiente configuradas
- [ ] HTTPS funcionando

## 🎉 Pronto!

Sua aplicação está no ar! 🚀

**URL da aplicação:** `https://meu-passaporte-pf.herokuapp.com`
