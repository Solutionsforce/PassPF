# 🚀 DEPLOY NO HEROKU - GUIA RÁPIDO

## ✅ Projeto Preparado!

Todos os arquivos necessários foram criados e configurados. O projeto está pronto para deploy!

## 📋 Comandos para Deploy (Copie e Cole)

### 1️⃣ Instalar Heroku CLI

**Windows:** https://devcenter.heroku.com/articles/heroku-cli  
**Mac:** `brew tap heroku/brew && brew install heroku`  
**Linux:** `curl https://cli-assets.heroku.com/install.sh | sh`

### 2️⃣ Fazer Deploy

```bash
# Login no Heroku
heroku login

# Criar aplicação (substitua 'meu-passaporte' pelo nome desejado)
heroku create meu-passaporte

# Configurar variáveis de ambiente (IMPORTANTE!)
# Gere uma chave segura:
python -c "import secrets; print(secrets.token_hex(32))"

# Configure as variáveis (cole a chave gerada acima):
heroku config:set SESSION_SECRET="cole_a_chave_gerada_aqui"
heroku config:set FOURM_PAYMENTS_API_TOKEN="seu_token_4m_aqui"

# Deploy! (use git push heroku main ou master)
git push heroku main

# Abrir no navegador
heroku open

# Ver logs
heroku logs --tail
```

## 🔒 Variáveis de Ambiente Necessárias

| Variável | Onde Conseguir | Obrigatória |
|----------|----------------|-------------|
| `SESSION_SECRET` | Gere com: `python -c "import secrets; print(secrets.token_hex(32))"` | ✅ SIM |
| `FOURM_PAYMENTS_API_TOKEN` | Painel 4M Payments: https://app.4mpagamentos.com | ✅ SIM |

## 📁 Arquivos Criados

✅ **Procfile** - Configuração do servidor Gunicorn  
✅ **runtime.txt** - Versão do Python (3.11.13)  
✅ **requirements.txt** - Dependências (com gunicorn)  
✅ **.gitignore** - Proteção de arquivos sensíveis  
✅ **.env.example** - Template de variáveis de ambiente  
✅ **README.md** - Documentação completa  
✅ **DEPLOY_INSTRUCTIONS.md** - Instruções detalhadas  
✅ **SECURITY.md** - Guia de segurança  

## 🔐 Segurança Garantida

✅ Nenhuma chave de API exposta no código  
✅ Todas as chaves em variáveis de ambiente  
✅ .gitignore protegendo arquivos sensíveis  
✅ .env.example como documentação (sem valores reais)  

## ⚡ Status do Projeto

- ✅ Backend Flask funcionando
- ✅ Frontend responsivo
- ✅ Integração 4M Payments configurada
- ✅ Sistema de sessões seguro
- ✅ Geração de PDF
- ✅ Agendamento de unidades
- ✅ Pagamento PIX com QR Code
- ✅ Verificação automática de pagamento
- ✅ Pronto para produção!

## 🎯 Próximos Passos

1. Execute os comandos acima
2. Acesse sua aplicação
3. Teste o fluxo completo
4. Configure domínio personalizado (opcional)

## 💡 Dicas

- Use `heroku logs --tail` para debug em tempo real
- Configure SSL automático (Heroku já faz isso)
- Monitore uso de recursos no dashboard Heroku
- Para produção séria, considere plano pago (evita sleep)

## 📞 Comandos Úteis

```bash
# Ver status
heroku ps

# Reiniciar app
heroku restart

# Ver variáveis configuradas
heroku config

# Abrir dashboard
heroku dashboard

# Ver logs
heroku logs --tail
```

---

**Tudo pronto para o deploy! 🚀**

Qualquer dúvida, consulte o **DEPLOY_INSTRUCTIONS.md** para mais detalhes.
